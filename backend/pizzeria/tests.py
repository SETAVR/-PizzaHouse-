from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Favorite, Order, OrderItem, Pizza


User = get_user_model()


class PizzeriaApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password123")
        self.admin = User.objects.create_user(
            username="admin",
            password="password123",
            is_staff=True,
        )
        self.category = Category.objects.create(
            title="Classic",
            slug="classic",
            description="Classic pizzas",
        )
        self.pizza = Pizza.objects.create(
            title="Margherita",
            slug="margherita",
            description="Tomato sauce, mozzarella and basil",
            price=Decimal("450.00"),
            category=self.category,
        )

    def test_guest_can_read_pizzas_but_cannot_create_pizza(self):
        list_response = self.client.get(reverse("pizza-list"))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["results"][0]["title"], self.pizza.title)

        create_response = self.client.post(
            reverse("pizza-list"),
            {
                "title": "Admin only pizza",
                "slug": "admin-only",
                "description": "Only staff can create this",
                "price": "500.00",
                "category": self.category.id,
            },
            format="json",
        )

        self.assertIn(
            create_response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )
        self.assertFalse(Pizza.objects.filter(slug="admin-only").exists())

    def test_user_can_create_order_and_backend_calculates_total(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("create_order"),
            {
                "phone": "+79990000000",
                "address": "Test street, 1",
                "items": [
                    {
                        "pizza_id": self.pizza.id,
                        "quantity": 2,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, Decimal("900.00"))
        self.assertEqual(order.items.count(), 1)

        item = OrderItem.objects.get(order=order)
        self.assertEqual(item.pizza, self.pizza)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal("450.00"))

    def test_favorite_toggle_adds_and_removes_pizza(self):
        self.client.force_authenticate(self.user)

        first_response = self.client.post(
            reverse("toggle_favorite"),
            {"pizza_id": self.pizza.id},
            format="json",
        )

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertTrue(first_response.data["is_favorite"])
        self.assertTrue(Favorite.objects.filter(user=self.user, pizza=self.pizza).exists())

        second_response = self.client.post(
            reverse("toggle_favorite"),
            {"pizza_id": self.pizza.id},
            format="json",
        )

        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertFalse(second_response.data["is_favorite"])
        self.assertFalse(Favorite.objects.filter(user=self.user, pizza=self.pizza).exists())

    @patch("pizzeria.views.start_order_status_thread")
    @patch("pizzeria.views.send_order_status")
    def test_pay_order_marks_order_as_paid_and_starts_status_updates(
        self,
        send_order_status_mock,
        start_order_status_thread_mock,
    ):
        self.client.force_authenticate(self.user)
        order = Order.objects.create(
            user=self.user,
            phone="+79990000000",
            address="Test street, 1",
            total_price=Decimal("450.00"),
        )

        response = self.client.post(reverse("pay_order", kwargs={"pk": order.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertTrue(order.is_paid)
        self.assertEqual(order.status, Order.Status.PAID)
        send_order_status_mock.assert_called_once_with(order)
        start_order_status_thread_mock.assert_called_once_with(order.id)
