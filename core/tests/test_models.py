"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from decimal import Decimal


def create_seller(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_seller_with_email_successful(self):
        """Test create a seller with an email is successfull."""
        email = 'test@example.com'
        password = 'testpass123'

        seller = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(seller.email, email)
        self.assertTrue(seller.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new sellers"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            seller = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(seller.email, expected)

    def test_new_seller_without_email_raises_error(self):
        """Test that creating a seller without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        """Test creating superuser"""
        seller = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(seller.is_superuser)
        self.assertTrue(seller.is_staff)

    def test_create_credit_request(self):
        """Test creating a credit request successfull."""
        seller = create_seller()
        credit_request = models.CreditRequest.objects.create(
            seller=seller,
            requested_credit_amount=Decimal('10.05')
        )

        credit_exist = models.CreditRequest.objects.get(
            seller=seller,
            requested_credit_amount=Decimal('10.05')
        )

        self.assertTrue(credit_exist)

    def test_create_phone_number(self):
        """Test creating a phone number successfull."""
        number = '+989123456789'
        charge = Decimal('1000')

        ph = models.PhoneNumber.objects.create(
            phone_number=number, charge=charge)

        self.assertEqual(ph.phone_number, number)
        self.assertEqual(ph.charge, charge)

    def test_create_charge_request(self):
        """Test creating a charge request successfull."""
        seller = create_seller()
        phone_number = models.PhoneNumber.objects.create(
            phone_number='+989112345678'
        )
        amount = Decimal('2000')
        request = models.ChargeRequest.objects.create(
            seller=seller,
            phone_number=phone_number,
            requested_credit_amount=amount
        )

        self.assertEqual(request.seller, seller)
        self.assertEqual(request.phone_number, phone_number)
        self.assertEqual(request.requested_credit_amount, amount)

    def test_create_transaction(self):
        """Test creating a transation successfull."""
        seller = create_seller()
        transaction_amount = Decimal('10000')
        transaction = models.Transaction.objects.create(
            seller=seller,
            amount=transaction_amount,
            credit_before_transaction=seller.credit,
            credit_after_transaction=seller.credit+transaction_amount
        )

        self.assertEqual(transaction.seller, seller)
        self.assertEqual(transaction.amount, transaction_amount)
