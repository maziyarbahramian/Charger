"""Services for request API Views."""
from django.db import transaction
from core.models import (
    Seller,
    CreditRequest,
    ChargeRequest,
    Transaction
)


class RequestService:
    """
    A singleton service providing methods for 
        - Depositing and withdrawing seller credit
        - Charge phone numbers.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestService, cls).__new__(cls)
        return cls._instance

    def create_credit_request(self, seller_id, amount):
        """save seller's credit request"""
        request = CreditRequest.objects.create(
            seller_id=seller_id,
            amount=amount
        )
        return request

    def ـdeposit(self, seller, request):
        """depositing to the seller credit."""
        return Transaction.objects.create(
            seller=request.seller,
            amount=request.amount,
            credit_before_transaction=seller.credit,
            credit_after_transaction=seller.credit+request.amount,
            type=Transaction.Type.DEPOSIT,
            detail=f'{request.__class__.__name__}-{request.id}'
        )

    def ـwithdraw(self, seller, request):
        """withdraw from seller credit."""
        return Transaction.objects.create(
            seller=seller,
            amount=-request.amount,
            credit_before_transaction=seller.credit,
            credit_after_transaction=seller.credit-request.amount,
            type=Transaction.Type.WITHDRAW,
            detail=f'{request.__class__.__name__}-{request.id}'
        )

    def accept_credit_request(self, request_id):
        """accept credit request and add requested amount to seller credit"""
        with transaction.atomic():
            request = CreditRequest.objects.get(id=request_id)

            if request.status != CreditRequest.Status.PENDING:
                raise CreditRequest.AlreadyProcessedError

            request.status = CreditRequest.Status.ACCEPTED
            request.save()
            seller = Seller.objects.get_queryset() \
                .filter(id=request.seller.id).select_for_update(nowait=True).get()

            transaction_obj = self.ـdeposit(seller, request)

            seller.credit += request.amount
            seller.save()
            return transaction_obj

    def reject_credit_request(self, request_id):
        """reject credit request"""
        with transaction.atomic():
            request = CreditRequest.objects.get_queryset() \
                .filter(id=request_id).select_for_update(nowait=True).get()

            if request.status != CreditRequest.Status.PENDING:
                raise CreditRequest.AlreadyProcessedError

            request.status = CreditRequest.Status.REJECTED
            request.save()
            return request

    def charge_phone_number(self, seller_id, phone_number, amount):
        """Charge the specified phone number."""
        with transaction.atomic():
            seller = Seller.objects.get_queryset() \
                .filter(id=seller_id).select_for_update(nowait=True).get()

            if seller.credit < amount:
                raise Seller.InsufficientCreditError

            request = ChargeRequest.objects.create(
                seller=seller,
                phone_number=phone_number,
                amount=amount
            )
            transaction_obj = self.ـwithdraw(seller, request)
            seller.credit -= amount
            seller.save()

            return transaction_obj
