"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class SellerManager(BaseUserManager):
    """Manager for sellers."""

    def create_user(self, email, password=None, **extra_fields):
        """create, save and return a new seller."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Seller(AbstractBaseUser, PermissionsMixin):
    """Seller in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    about = models.TextField()
    credit = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 null=True,
                                 blank=True,
                                 default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SellerManager()

    USERNAME_FIELD = 'email'

    class InsufficientCreditError(Exception):
        def __init__(self, message="Seller credit is insufficient."):
            self.message = message
            super().__init__(self.message)

    def __str__(self) -> str:
        return self.name


class CreditRequest(models.Model):
    """model for credit requests."""
    class Status(models.TextChoices):
        PENDING = ('Pending', 'Pending')
        ACCEPTED = ('Accepted', 'Accepted')
        REJECTED = ('Rejected', 'Rejected')

    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    request_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    def __str__(self) -> str:
        return (
            f'Credit Request - Seller: {self.seller}, '
            f'Amount: {self.amount}, '
            f'Request Time: {self.request_time}, '
            f'Status: {self.get_status_display()}'
        )

    class AlreadyProcessedError(Exception):
        def __init__(self, message="This request has already been processed and cannot be accepted or rejected again."):
            self.message = message
            super().__init__(self.message)


class ChargeRequest(models.Model):
    """model for charge requests."""
    seller = models.ForeignKey('seller', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f'Charge Request - Seller: {self.seller}, '
            f'Phone Number: {self.phone_number}, '
            f'Amount: {self.amount}, '
            f'Request Time: {self.request_time}'
        )


class Transaction(models.Model):
    """model for all of deposit and withdraw transactions."""
    class Type(models.TextChoices):
        WITHDRAW = ('Withdraw', 'Withdraw')
        DEPOSIT = ('Deposit', 'Deposit')

    seller = models.ForeignKey('seller', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    credit_before_transaction = models.DecimalField(
        max_digits=10, decimal_places=2)
    credit_after_transaction = models.DecimalField(
        max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=10,
        choices=Type.choices
    )
    detail = models.TextField()
    transaction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f'Transaction Type: {self.get_type_display()}, '
            f'Amount: {self.amount}, '
            f'Credit Before Transaction: {self.credit_before_transaction}, '
            f'Credit After Transaction: {self.credit_after_transaction}, '
            f'Detail: {self.detail}, '
            f'Transaction Time: {self.transaction_time}'
        )
