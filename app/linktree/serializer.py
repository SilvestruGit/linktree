"""
Serializers for LinkTree APIs.
"""
from rest_framework import serializers

from core.models import LinkTree


class LinkTreeSerializer(serializers.ModelSerializer):
    """Serializer for linktrees."""

    class Meta:
        model = LinkTree
        fields = ['id', 'title', 'link']
        read_only_fields = ['id']
