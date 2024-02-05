"""
Test for APIs.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import (
    CreditRequest
)

def create_credit_request():
    pass

class CreditRequestTest(TestCase):
    pass