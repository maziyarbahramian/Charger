"""
Serializers for requests API Views.
"""
from rest_framework import serializers
from django.core.validators import MinValueValidator
from core.models import (
    CreditRequest,
    Seller,
    Transaction
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


class AcceptCreditRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditRequest.objects.values_list('id', flat=True).all(),
        write_only=True
    )

    class Meta:
        model = Transaction
        fields = ['id', 'request_id', 'seller', 'amount', 'credit_before_transaction',
                  'credit_after_transaction', 'type', 'detail']
        read_only_fields = ['id', 'seller', 'amount', 'credit_before_transaction',
                            'credit_after_transaction', 'type', 'detail']


class ChargePhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'seller', 'credit_before_transaction',
                            'credit_after_transaction', 'type', 'detail']
        extra_kwargs = {
            'amount': {
                'validators': [
                    MinValueValidator(
                        limit_value=0.01)
                ]
            },
        }


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = '__all__'
