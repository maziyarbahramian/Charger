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
    credit = models.DecimalField(max_digits=6,
                                 decimal_places=2,
                                 null=True,
                                 blank=True,
                                 default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SellerManager()

    USERNAME_FIELD = 'email'
