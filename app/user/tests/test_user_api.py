"""
Tests for the user API.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a user."""
    user = get_user_model().objects.create_user(
        'test@example.com',
        'parola1234',
        username='Test Username',
    )

    return user


class UnauthenticatedUsersTests(TestCase):
    """Tests for unauthenticated users."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a new user is successful."""
