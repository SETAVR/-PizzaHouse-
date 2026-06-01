from django.db import transaction
from rest_framework import serializers

from .models import Category, Favorite, Order, OrderItem, Pizza, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "slug", "description", "is_active")


class PizzaSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Pizza
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "price",
            "image",
            "is_available",
            "category",
            "category_title",
            "created_at",
            "updated_at",
        )


class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "pizza", "author", "author_username", "text", "rating", "created_at")
        read_only_fields = ("pizza", "author")


class FavoriteSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "pizza", "created_at")


class FavoriteToggleSerializer(serializers.Serializer):
    pizza_id = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):
    pizza_title = serializers.CharField(source="pizza.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "pizza", "pizza_title", "quantity", "price")


class OrderCreateItemSerializer(serializers.Serializer):
    pizza_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderCreateItemSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = ("id", "phone", "address", "items")

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Cart cannot be empty.")
        pizza_ids = [item["pizza_id"] for item in value]
        available_ids = set(Pizza.objects.filter(pk__in=pizza_ids, is_available=True).values_list("id", flat=True))
        missing_ids = set(pizza_ids) - available_ids
        if missing_ids:
            raise serializers.ValidationError("Some pizzas are unavailable or do not exist.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        cart_items = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(user=user, **validated_data)

        total_price = 0
        for item in cart_items:
            pizza = Pizza.objects.select_for_update().get(pk=item["pizza_id"], is_available=True)
            quantity = item["quantity"]
            OrderItem.objects.create(
                order=order,
                pizza=pizza,
                quantity=quantity,
                price=pizza.price,
            )
            total_price += pizza.price * quantity

        order.total_price = total_price
        order.save(update_fields=["total_price"])
        return order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "phone",
            "address",
            "total_price",
            "status",
            "is_paid",
            "created_at",
            "updated_at",
            "items",
        )
