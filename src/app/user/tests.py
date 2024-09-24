from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.app.user.models import User


# Create your tests here.
class AuthTest(APITestCase):
    def setUp(self):
        User.objects.create_superuser(
            username="test",
            password="test",
            email="test@test.com"
        )

    def test_signin(self):
        url = reverse('signin')
        data = {
            "username": "test",
            "password": "test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup(self):
        url = reverse('signup')
        data = {
            "username": "teasdfsadfst",
            "email": "test@gmail.com",
            "password": "tesasdft"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
