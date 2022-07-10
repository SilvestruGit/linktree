"""
Tests for the user API.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a user."""
    user = get_user_model().objects.create_user(
        email='test@example.com',
        password='parola1234',
        username='Test Username',
    )

    return user


class UnauthenticatedUsersTests(TestCase):
    """Tests for unauthenticated users."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a new user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'parola1234',
            'username': 'Test User',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(user.email, res.data['email'])
        self.assertEqual(user.username, res.data['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_user_with_email_exists_error(self):
        """Test creating a user with an existing email raises error."""
        payload = {
            'email': 'test@example.com',
            'password': 'parola1234',
            'username': 'Test User',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        users_count = get_user_model().objects.filter(
            email=payload['email']
        ).count()

        self.assertEqual(users_count, 1)

    def test_password_to_short(self):
        """Test password to short raises error. Less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': '1234',
            'username': 'Test User',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test creating a auth token for a user."""
        user_details = {
            'email': 'test@example.com',
            'password': 'parola1234',
            'username': 'Test Username'
        }
        create_user(**user_details)

        payload = {
            'email': 'test@example.com',
            'password': 'parola1234',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data)
        self.assertIn('token', res.data)

    def test_create_token_With_bad_inputs(self):
        """Test creating a token with bad inputs raises an error."""
        user_details = {
            'email': 'test@example.com',
            'password': 'parola1234',
            'username': 'Test Username'
        }
        create_user(**user_details)

        payload = {
            'email': 'wrong@test.com',
            'password': 'wrong_pass',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_with_blank_password(self):
        """Test creating a token with a blank password raises error."""
        payload = {
            'email': 'wrong@test.com',
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrive_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    """Tests for authenticated users."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retirve_profile(self):
        """Test using the ME endpoint."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, res.data['email'])

    def test_post_me_not_allowed(self):
        """Test POST is not allowed from ME endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile."""
        payload = {
            'username': 'New name',
            'password': 'newpass1234'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], payload['username'])
        self.assertTrue(self.user.check_password(payload['password']))
