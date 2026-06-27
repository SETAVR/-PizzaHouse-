from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Category, Favorite, Order, Pizza, Review
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    FavoriteSerializer,
    FavoriteToggleSerializer,
    FavoriteToggleResponseSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    PizzaSerializer,
    ReviewSerializer,
)
from .services import send_order_status, start_order_status_thread


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.select_related("category").all()
    serializer_class = PizzaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    @action(detail=True, methods=["get", "post"], permission_classes=[permissions.AllowAny])
    def reviews(self, request, pk=None):
        pizza = self.get_object()
        if request.method == "GET":
            reviews = pizza.reviews.select_related("author").all()
            return Response(ReviewSerializer(reviews, many=True).data)
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(pizza=pizza, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(responses=FavoriteSerializer(many=True))
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_favorites(request):
    favorites = Favorite.objects.select_related("pizza", "pizza__category").filter(user=request.user)
    return Response(FavoriteSerializer(favorites, many=True).data)


@extend_schema(
    request=FavoriteToggleSerializer,
    responses=FavoriteToggleResponseSerializer,
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request):
    serializer = FavoriteToggleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    pizza = get_object_or_404(Pizza, pk=serializer.validated_data["pizza_id"])
    favorite, created = Favorite.objects.get_or_create(user=request.user, pizza=pizza)
    if not created:
        favorite.delete()
    return Response({"is_favorite": created})


@extend_schema(responses=OrderSerializer(many=True))
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_orders(request):
    orders = Order.objects.prefetch_related("items__pizza").filter(user=request.user)
    return Response(OrderSerializer(orders, many=True).data)


@extend_schema(request=OrderCreateSerializer, responses=OrderSerializer)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    order = serializer.save()
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@extend_schema(responses=OrderSerializer)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items__pizza"), pk=pk, user=request.user)
    return Response(OrderSerializer(order).data)


@extend_schema(request=None, responses=OrderSerializer)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def pay_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.is_paid:
        return Response(OrderSerializer(order).data)
    order.is_paid = True
    order.status = Order.Status.PAID
    order.save(update_fields=["is_paid", "status", "updated_at"])
    send_order_status(order)
    start_order_status_thread(order.id)
    return Response(OrderSerializer(order).data)
