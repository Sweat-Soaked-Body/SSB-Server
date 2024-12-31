import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


@pytest.fixture
def client():
    return APIClient()

class TestSignUp:
    @patch('user.models.ServiceUser.objects.create_user')
    @patch('userprofile.models.ServiceUserProfile.objects.create')
    def test_signup(self, mock_create_user, mock_create_profile, client):
        mock_create_user_data = {
            'username': 'testusername',
            'password': 'testpassword',
        }
        mock_create_user.return_value = mock_create_user_data

        mock_create_profile_data = {
            'service_user': mock_create_user_data,
            'name': 'testname',
            'sex': 'M',
            'age': 20,
            'weight': 70,
            'height': 170,
        }
        mock_create_profile.return_value = mock_create_profile_data

        response = client.post(reverse('signup'), data=mock_create_user_data)
        self.assertEqual(response.status_code, 201)
        