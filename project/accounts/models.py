""" 
User model.

Using the Django User model as a base model, we extend it to add more fields to it.
Also the BaseUserManager acts as a manager for the User model. It is used to create
a user. The create_user method creates a normal user. The create_superuser method
creates a superuser.
"""

# Native imports
import random
import string

# Django imports
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """ Manager for the User model """

    use_in_migrations = True

    def _generate_username(self):
        """ Generate a random username """
        return ''.join(random.choice(string.ascii_letters) for i in range(10))

    def _generate_tag(self):
        """ Generate a 4 digit random tag """
        return ''.join(random.choice(string.digits) for i in range(4))

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the email and password."""

        # Check if email is provided
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_email_user(self, email=None, password=None, **extra_fields):
        """ Method to create a email user """
        extra_fields.setdefault(
            'is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """ Method to create a super user """

        extra_fields.setdefault(
            'is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ User Abstract model """

    # Information
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
