"""
Serializers for the seller API View
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers


class SellerSerializer(serializers.ModelSerializer):
    """Serializer for the seller object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'about']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'about': {'required': False}
        }

    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the seller auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the seller."""
        email = attrs.get('email')
        password = attrs.get('password')
        seller = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not seller:
            msg = 'Unable to authenticate with provided credentials.'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = seller
        return attrs
