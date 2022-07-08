"""
Views for the User API.
"""

from rest_framework import generics
from user.serializer import (
    UserSerializer,
    TokenSerializer,
)


class CreateUsersView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(generics.CreateApiView):
    """Create a new token for the user."""
    serializer_class = TokenSerializer
