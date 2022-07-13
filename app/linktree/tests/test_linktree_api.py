"""
Tests for LinkTree APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models

from linktree import serializer


LINK_URL = reverse('linktree:linktree-list')


def create_linktree(user, **params):
    """Create and return a sample linktree."""
    defaults = {
        'title': 'Test Title',
        'link': 'https://github.com/',
    }

    defaults.update(params)

    linktree = models.LinkTree.objects.create(user=user, **defaults)
    return linktree


class PublicLinkTreeTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test the user must be authenticated to call API."""
        res = self.client.get(LINK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test for authenticated users."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='Parola1234',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_links(self):
        """Test retrieving a list of links."""
        create_linktree(user=self.user)
        create_linktree(user=self.user)

        res = self.client.get(LINK_URL)

        links = models.LinkTree.objects.all().order_by('-id')
        link_serializer = serializer.LinkTreeSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, link_serializer.data)

    def test_retrieve_links_for_auth_user_only(self):
        """Test get links for the auth user only."""
        user2 = get_user_model().objects.create_user(
            email='other@example.com',
            password='parola124',
        )
        create_linktree(user=user2)

        create_linktree(user=self.user)
        create_linktree(user=self.user)

        res = self.client.get(LINK_URL)

        links = models.LinkTree.objects.filter(user=self.user).order_by('-id')
        link_serializer = serializer.LinkTreeSerializer(links, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, link_serializer.data)
