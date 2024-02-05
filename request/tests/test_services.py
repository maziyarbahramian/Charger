"""
Tests for request services.
"""
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from request.services import RequestService
from django.db import transaction
from decimal import Decimal
from core.models import (
    CreditRequest,
    PhoneNumber,
    ChargeRequest,
    Seller,
    Transaction
)


class ServiceTest(TransactionTestCase):

    def setUp(self):
        self.seller = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            credit=Decimal('100.00')
        )
        self.service = RequestService()

    def test_create_credit_request(self):
        """test create a credit request."""
        request_amount = Decimal('50.00')
        request = self.service.create_credit_request(
            seller_id=self.seller.id,
            amount=request_amount
        )

        self.assertEqual(request.amount, request_amount)
        self.assertEqual(request.status, CreditRequest.Status.PENDING)

    def test_accept_credit_request_success(self):
        """Test accept a credit request successfull."""
        request_amount = Decimal('50.00')
        request = self.service.create_credit_request(
            seller_id=self.seller.id,
            amount=request_amount
        )

        transaction = self.service.accept_credit_request(request.id)

        self.assertEqual(transaction.credit_before_transaction,
                         self.seller.credit)
        self.assertEqual(transaction.credit_after_transaction,
                         self.seller.credit+request_amount)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, Decimal('150.00'))

    def test_accept_credit_request_failed(self):
        """Test accept a already processed credit request failed."""
        request = CreditRequest.objects.create(
            seller=self.seller,
            amount=Decimal('50.00'),
            status=CreditRequest.Status.SUCCESS,
        )

        with self.assertRaises(CreditRequest.AlreadyProcessedError):
            self.service.accept_credit_request(request.id)

    def test_reject_credit_request(self):
        """Test reject a credit request."""
        request_amount = Decimal('50.00')
        request = self.service.create_credit_request(
            seller_id=self.seller.id,
            amount=request_amount
        )
        self.service.reject_credit_request(request_id=request.id)
        request.refresh_from_db()
        self.seller.refresh_from_db()

        self.assertEqual(self.seller.credit, Decimal('100.00'))
        self.assertEqual(request.status, CreditRequest.Status.FAILED)

    def test_charge_phone_number_success(self):
        """Test charge a phone number."""
        amount = Decimal('15.00')
        number = '+989114412191'
        phone_number = PhoneNumber.objects.create(
            number=number,
            charge=Decimal('5.00')
        )
        _, transaction = self.service.charge_phone_number(
            seller_id=self.seller.id,
            number=number,
            amount=amount
        )

        self.seller.refresh_from_db()
        phone_number.refresh_from_db()
        self.assertEqual(self.seller.credit, Decimal('85.00'))
        self.assertEqual(phone_number.charge, Decimal('20.00'))

    def test_charge_phone_number_success(self):
        """Test charge a phone number failed because of insufficient credit"""
        phone = PhoneNumber.objects.create(
            number='+989114412191',
            charge=Decimal('5.00')
        )
        with self.assertRaises(Seller.InsufficientCreditError):
            self.service.charge_phone_number(
                seller_id=self.seller.id,
                number=phone.number,
                amount=Decimal('150.00')
            )

        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, Decimal('100'))
