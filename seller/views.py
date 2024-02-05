"""
Views for the seller API.
"""
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from seller.serializers import (
    SellerSerializer,
    SellerDetailSerializer,
    AuthTokenSerializer,
)
from core.models import Seller


class CreateSellerView(generics.CreateAPIView):
    """Create a new seller in the system."""
    serializer_class = SellerSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for seller."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RetrieveSellerView(generics.RetrieveAPIView):
    """Get authenticated seller."""
    serializer_class = SellerDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class ListSellerViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Retrieve one item or List of sellers."""
    serializer_class = SellerDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Seller.objects.all()
