"""
Tests for models.
"""

from django.test import TestCase
from core import models
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):
    """Tests for models."""

    def test_create_user(self):
        """Test creating a user is succesful."""

        email = 'test@example.com'
        password = 'parola1234'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

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
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(email='', password='123')

    def test_create_superuser(self):
        """Test creating a superuser is succesful."""
        user = get_user_model().objects.create_superuser(
            'test@ezample.com',
            '1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_linktree(self):
        """Test creating a linktree model."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='parola1234',
        )
        linktree = models.LinkTree.objects.create(
            user=user,
            title='My linktree',
        )

        self.assertEqual(str(linktree), linktree.title)
