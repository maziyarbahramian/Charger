"""
Serializers for requests API Views.
"""
from rest_framework import serializers
from django.core.validators import MinValueValidator
from core.models import (
    CreditRequest,
    Seller,
)
from seller.serializers import SellerSerializer


class CreateCreditRequestSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(required=False, read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.values_list('id', flat=True).all(),
        write_only=True
    )

    class Meta:
        model = CreditRequest
        fields = ['id', 'seller', 'seller_id',
                  'amount', 'request_time', 'status']
        read_only_fields = ['request_time', 'status']
        extra_kwargs = {
            'amount': {'validators': [MinValueValidator(limit_value=0.01)]},
            'request_time': {'required': False, 'read_only': True},
            'status': {'required': False, 'read_only': True},
            'id': {'required': False, 'read_only': True},
        }
