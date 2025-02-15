import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from movies_api.apps.users.models import User

TOKEN_URL = reverse("token_obtain_pair")


def create_user(**params) -> User:
    return User.objects.create_user(**params)


@pytest.mark.django_db
class TestAuthApi:
    """Tests for the auth API"""

    def test_user_can_login(self, api_client: APIClient):
        """Test that user login success with valid credentials"""
        payload = {"email": "test@email.com", "password": "test123", "first_name": "jose"}
        create_user(**payload)
        res = api_client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_200_OK

    def test_user_login_fails_with_invalid_credentials(self, api_client: APIClient):
        """Test that user login fails with invalid credentials"""

        create_user(email="jv", password="test123")
        payload = {"email": "jv@email.com", "password": "wrong"}
        res = api_client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "payload",
        [
            ({"email": "test@email.com"},),
            ({"email": "test@email.com", "password": None}),
            ({"email": "test@email.com", "password": ""}),
            ({"email": "", "password": "1234455"}),
            ({"email": None, "password": "1234455"}),
            ({"password": "1234455"}),
        ],
    )
    def test_create_token_missing_field(self, api_client: APIClient, payload: dict):
        """Test that email and password are required"""
        response = api_client.post(TOKEN_URL, payload=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "token" not in response.data
