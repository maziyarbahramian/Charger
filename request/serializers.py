"""
Serializers for requests API Views.
"""
from rest_framework import serializers
from django.core.validators import MinValueValidator
from core.models import (
    CreditRequest,
    Transaction
)
from seller.serializers import SellerSerializer


class CreateCreditRequestSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(required=False)

    class Meta:
        model = CreditRequest
        fields = '__all__'
        read_only_fields = ['request_time', 'status']
        extra_kwargs = {
            'amount': {'validators': [MinValueValidator(limit_value=0.01)]},
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


class RejectCreditRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditRequest.objects.values_list('id', flat=True).all(),
        write_only=True
    )
    seller = SellerSerializer(required=False, read_only=True)

    class Meta:
        model = CreditRequest
        fields = '__all__'
        read_only_fields = ['seller', 'amount', 'request_time', 'status']


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
    seller = SellerSerializer()

    class Meta:
        model = CreditRequest
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
