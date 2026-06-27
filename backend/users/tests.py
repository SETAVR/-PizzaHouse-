from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationApiTests(APITestCase):
    def test_user_can_register_and_receive_jwt_tokens(self):
        register_response = self.client.post(
            reverse("register"),
            {
                "username": "new_user",
                "email": "new@example.com",
                "password": "strong-password-123",
                "phone": "+79990000000",
                "address": "Test street, 1",
            },
            format="json",
        )
        login_response = self.client.post(
            reverse("login"),
            {"username": "new_user", "password": "strong-password-123"},
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

    def test_authenticated_user_can_read_and_update_profile(self):
        user = User.objects.create_user(username="profile_user", password="password123")
        self.client.force_authenticate(user)

        profile_response = self.client.get(reverse("profile"))
        update_response = self.client.patch(
            reverse("profile"),
            {"phone": "+79991112233", "address": "Updated address"},
            format="json",
        )

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.phone, "+79991112233")
        self.assertEqual(user.address, "Updated address")
