from decimal import Decimal

from django.core.management.base import BaseCommand
from pizzeria.models import Category, Pizza


class Command(BaseCommand):
    help = "Create demo categories and pizzas."

    def handle(self, *args, **options):
        categories = {
            "classic": ("Классические", "Проверенные вкусы для знакомства с меню."),
            "spicy": ("Острые", "Пиццы с ярким соусом и перцем."),
            "meat": ("Мясные", "Сытные пиццы с мясными начинками."),
            "vegetarian": ("Вегетарианские", "Овощные пиццы без мяса."),
        }
        category_objects = {}
        for slug, (title, description) in categories.items():
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"title": title, "description": description},
            )
            category_objects[title] = category

        pizzas = [
            ("margherita", "Маргарита", "Классика с томатным соусом, моцареллой и базиликом.", "Классические", "450.00"),
            ("pepperoni", "Пепперони", "Моцарелла, томатный соус и пикантная пепперони.", "Острые", "590.00"),
            ("four-cheese", "Четыре сыра", "Моцарелла, дорблю, пармезан и сливочный сыр.", "Классические", "620.00"),
            ("meat", "Мясная", "Ветчина, бекон, курица, колбаски и сыр.", "Мясные", "690.00"),
            ("vegetarian", "Вегетарианская", "Томаты, перец, грибы, маслины и сыр.", "Вегетарианские", "540.00"),
        ]
        for slug, title, description, category_title, price in pizzas:
            Pizza.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": description,
                    "category": category_objects[category_title],
                    "price": Decimal(price),
                    "is_available": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data created."))
