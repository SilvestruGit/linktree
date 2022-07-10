"""
User serializer for the API view.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    """Serializer for the auth user token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs['email']
        password = attrs['password']
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if not user:
            msg = _('Unable to Authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
