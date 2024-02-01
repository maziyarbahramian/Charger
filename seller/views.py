"""
Views for the seller API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from seller.serializers import (
    SellerSerializer,
    AuthTokenSerializer,
)
from rest_framework.permissions import IsAuthenticated


class CreateSellerView(generics.CreateAPIView):
    """Create a new seller in the system."""
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for seller."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
