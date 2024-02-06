"""
Test for APIs.
"""
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import (
    CreditRequest,
    Seller
)

CREDIT_REQUEST_URL = reverse('request:credit-request')
ACCEPT_CREDIT_REQUEST_URL = reverse('request:accept-credit-request')
REJECT_CREDIT_REQUEST_URL = reverse('request:reject-credit-request')


def create_seller(email='email@test.com',
                  password='test1234',
                  is_staff=False):
    seller = Seller.objects.create_user(email=email, password=password)
    seller.is_staff = is_staff
    return seller


def create_credit_request(seller, amount):
    return CreditRequest.objects.create(
        seller=seller, amount=amount
    )


class CreateCreditRequestApiTests(APITestCase):
    """Test create credit request api."""

    def setUp(self):
        self.seller = create_seller()

    def test_auth_required(self):
        """Test auth is required for create a credit request"""
        res = self.client.post(CREDIT_REQUEST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_credit_request_success(self):
        self.client.force_authenticate(user=self.seller)
        payload = {
            'amount': 500.00
        }
        res = self.client.post(CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_request_zero_amount_failed(self):
        """Test create a credit request with amount=0 failed."""
        self.client.force_authenticate(user=self.seller)
        payload = {
            'amount': 0
        }
        res = self.client.post(CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_request_negative_amount_failed(self):
        """Test create a credit request with amount=-1 failed."""
        self.client.force_authenticate(user=self.seller)
        payload = {
            'amount': -1
        }
        res = self.client.post(CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AcceptCreditRequestApiTests(APITestCase):
    """Test accept credit request api."""

    def setUp(self):
        self.seller = create_seller()
        self.admin_seller = create_seller(
            email='admin@example.com',
            is_staff=True)
        self.credit_request = create_credit_request(
            self.seller, Decimal('50.0'))

    def test_accept_credit_request_failed(self):
        """Test accept credit request using normal user failed."""
        self.client.force_authenticate(user=self.seller)
        payload = {'request_id': self.credit_request.id}
        res = self.client.post(ACCEPT_CREDIT_REQUEST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_credit_request_success(self):
        """Test accept credit request success"""
        self.client.force_authenticate(user=self.admin_seller)
        payload = {'request_id': self.credit_request.id}

        res = self.client.post(ACCEPT_CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_accept_credit_request_twice_failed(self):
        """Test can't accept a credit request twice."""
        self.client.force_authenticate(user=self.admin_seller)
        payload = {'request_id': self.credit_request.id}

        self.client.post(ACCEPT_CREDIT_REQUEST_URL, payload)
        res = self.client.post(ACCEPT_CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)


class RejectCreditRequestApiTests(APITestCase):
    """Test reject credit request api."""

    def setUp(self):
        self.seller = create_seller()
        self.admin_seller = create_seller(
            email='admin@example.com',
            is_staff=True)
        self.credit_request = create_credit_request(
            self.seller, Decimal('50.0'))

    def test_reject_credit_request_failed(self):
        """Test reject credit request using normal user failed."""
        self.client.force_authenticate(user=self.seller)
        payload = {'request_id': self.credit_request.id}
        res = self.client.post(REJECT_CREDIT_REQUEST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_credit_request_success(self):
        """Test reject credit request success"""
        self.client.force_authenticate(user=self.admin_seller)
        payload = {'request_id': self.credit_request.id}

        res = self.client.post(REJECT_CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_reject_credit_request_twice_failed(self):
        """Test can't accept a credit request twice."""
        self.client.force_authenticate(user=self.admin_seller)
        payload = {'request_id': self.credit_request.id}

        self.client.post(REJECT_CREDIT_REQUEST_URL, payload)
        res = self.client.post(REJECT_CREDIT_REQUEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)
