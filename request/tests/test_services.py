"""
Tests for request services.
"""
import threading
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from request.services import RequestService
from django.db import transaction
from decimal import Decimal
from core.models import (
    CreditRequest,
    Seller,
)


def create_seller(email='email@test.com',
                  password='test1234',
                  is_staff=False,
                  credit=Decimal('0')):
    seller = get_user_model().objects.create_user(
        email=email, password=password, credit=credit)
    seller.is_staff = is_staff
    return seller


def create_credit_request(seller, amount):
    return CreditRequest.objects.create(
        seller=seller, amount=amount
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
            status=CreditRequest.Status.ACCEPTED,
        )

        with self.assertRaises(CreditRequest.AlreadyProcessedError):
            self.service.accept_credit_request(request.id)

    def test_reject_credit_request_success(self):
        """Test reject a credit request successfull."""
        request_amount = Decimal('50.00')
        request = self.service.create_credit_request(
            seller_id=self.seller.id,
            amount=request_amount
        )
        self.service.reject_credit_request(request_id=request.id)
        request.refresh_from_db()
        self.seller.refresh_from_db()

        self.assertEqual(self.seller.credit, Decimal('100.00'))
        self.assertEqual(request.status, CreditRequest.Status.REJECTED)

    def test_reject_credit_request_failed(self):
        """Test reject a credit request failed."""
        request = CreditRequest.objects.create(
            seller=self.seller,
            amount=Decimal('50.00'),
            status=CreditRequest.Status.ACCEPTED,
        )

        with self.assertRaises(CreditRequest.AlreadyProcessedError):
            self.service.reject_credit_request(request_id=request.id)

    def test_charge_phone_number_success(self):
        """Test charge a phone number."""
        amount = Decimal('15.00')
        number = '+989114412191'

        transaction = self.service.charge_phone_number(
            seller_id=self.seller.id,
            phone_number=number,
            amount=amount
        )

        self.seller.refresh_from_db()
        self.assertEqual(transaction.amount, -amount)
        self.assertEqual(self.seller.credit, Decimal('85.00'))

    def test_charge_phone_number_failed(self):
        """Test charge a phone number failed because of insufficient credit"""
        phone_number = '+989114412191'

        with self.assertRaises(Seller.InsufficientCreditError):
            self.service.charge_phone_number(
                seller_id=self.seller.id,
                phone_number=phone_number,
                amount=Decimal('150.00')
            )

        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, Decimal('100'))


class ServiceParallelTest(TransactionTestCase):
    """Test case for parallel execution of atomic funcions on service."""

    def setUp(self):
        self.seller = create_seller(credit=Decimal('100'))
        self.requests = []
        for _ in range(5):
            self.requests.append(
                create_credit_request(self.seller, Decimal(50))
            )

        self.service = RequestService()

    def test_parallel_accept_credit_request(self):
        """Test the parallel acceptance of credit requests."""
        threads = []
        for request in self.requests:
            thread = threading.Thread(
                target=self.service.accept_credit_request, args=(request.id,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.seller.refresh_from_db()
        expected_credit = Decimal('350')
        self.assertEqual(self.seller.credit, expected_credit)

    def test_parallel_reject_credit_request(self):
        """Test the parallel rejection of credit requests."""
        threads = []
        for request in self.requests:
            thread = threading.Thread(
                target=self.service.reject_credit_request, args=(request.id,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        expected_credit = self.seller.credit
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, expected_credit)
