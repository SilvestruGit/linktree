"""
Test django admin functionality.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status


class AdminSiteTests(TestCase):
    """Tests for admin site."""

    def setUp(self):
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='1234'
        )
        self.client.force_login(self.superuser)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='123',
            username='Suuu',
        )

    def test_users_list(self):
        """Test users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.username)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.username)

    def test_crest_user_page(self):
        """Test creating new user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
