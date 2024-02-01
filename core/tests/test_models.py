"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


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
