from django.test import TestCase
from rest_framework.test import APIClient
from .models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", firstname="John", lastname="Doe", password="password123"
        )

    def test_login(self):
        response = self.client.post("/api/user/login/", {"email": "test@example.com", "password": "password123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_user_info(self):
        login_response = self.client.post("/api/user/login/", {"email": "test@example.com", "password": "password123"})
        token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/user/info/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_logout(self):
        login_response = self.client.post("/api/user/login/", {"email": "test@example.com", "password": "password123"})
        print(login_response.data)
        token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        refresh = login_response.data["refresh"]
        response = self.client.post("/api/user/logout/", {"refresh": refresh})
        self.assertEqual(response.status_code, 200)
