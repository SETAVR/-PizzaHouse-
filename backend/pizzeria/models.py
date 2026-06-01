from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Pizza(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="pizzas/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name="pizzas", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Создан"
        PAID = "paid", "Оплачен"
        COOKING = "cooking", "Готовится"
        BAKING = "baking", "Выпекается"
        DELIVERING = "delivering", "Передан курьеру"
        COMPLETED = "completed", "Доставлен"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.pizza} x {self.quantity}"


class Review(models.Model):
    pizza = models.ForeignKey(Pizza, related_name="reviews", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pizza} review by {self.author}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="favorites", on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, related_name="favorites", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "pizza"], name="unique_user_pizza_favorite")
        ]

    def __str__(self):
        return f"{self.user} likes {self.pizza}"
