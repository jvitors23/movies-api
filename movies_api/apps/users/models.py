from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from movies_api.apps.core.models import BaseModel


class UserManager(BaseUserManager):
    """
    Custom user manager
    """

    def create_user(self, email: str, password: str | None = None, **extra_fields: dict[Any, Any]) -> "User":
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: dict[Any, Any]) -> "User":
        """
        Create and save a superupser with the given email and password
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractUser, BaseModel):
    """
    Custom user model that supports email instead of username
    """

    email = models.EmailField(max_length=255, unique=True)

    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: list[str] = []
