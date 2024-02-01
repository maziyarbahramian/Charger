"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_SELLER_URL = reverse('seller:create')
TOKEN_URL = reverse('seller:token')


def create_seller(**params):
    """Create and return a seller."""
    return get_user_model().objects.create_user(**params)


class PublicSellerApiTests(TestCase):
    """Tests the public features of the seller API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_seller_success(self):
        """Test creatign a seller is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_SELLER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        seller = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(seller.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_seller_with_email_exists_error(self):
        """Test error returned if seller with email already exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_seller(**payload)
        res = self.client.post(CREATE_SELLER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error returned if password less than 5 characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_SELLER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        seller_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(seller_exists)

    def test_create_token_for_seller(self):
        """Test generates a token for valid credentials."""
        seller_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-seller-password',
        }
        create_seller(**seller_details)

        payload = {
            'email': seller_details['email'],
            'password': seller_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials are invalid"""
        create_seller(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """Testing posting a blank password returns an error"""
        payload = {'email': 'test@exmaple.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
