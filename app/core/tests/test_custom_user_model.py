"""
Tests for the custom user model.
"""

from django.contrib.auth import get_user_model

from django.test import TestCase


class UserTests(TestCase):
    """Tests for the custom user model."""

    def test_create_user(self):
        """Test creating a user is succesful."""

        email = 'test@example.com'
        password = 'parola1234'

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """Test normalize email adresses."""
        emails = [
            ['TEST@EXAMPLE.COM', 'TEST@example.com'],
            ['Test@examPle.com', 'Test@example.com'],
            ['test@example.COM', 'test@example.com'],
        ]

        for email, expected in emails:
            user = get_user_model().objects.create_user(email)
            self.assertEqual(user.email, expected)

    def test_create_user_with_no_email_error(self):
        """Test creating a new user with no email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='123')

    def test_create_superuser(self):
        """"""
