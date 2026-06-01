# Generated for the PizzaHouse course project.

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("slug", models.SlugField(max_length=140, unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "categories",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Pizza",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("slug", models.SlugField(max_length=180, unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("image", models.ImageField(blank=True, null=True, upload_to="pizzas/")),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="pizzas", to="pizzeria.category"),
                ),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(max_length=30)),
                ("address", models.CharField(max_length=255)),
                ("total_price", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Создан"),
                            ("paid", "Оплачен"),
                            ("cooking", "Готовится"),
                            ("baking", "Выпекается"),
                            ("delivering", "Передан курьеру"),
                            ("completed", "Доставлен"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                ("is_paid", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "pizza",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="pizzeria.pizza"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "order",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="pizzeria.order"),
                ),
                (
                    "pizza",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_items", to="pizzeria.pizza"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "pizza",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="pizzeria.pizza"),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(fields=("user", "pizza"), name="unique_user_pizza_favorite"),
        ),
    ]
