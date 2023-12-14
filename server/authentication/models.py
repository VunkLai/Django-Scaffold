from __future__ import annotations

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class Manager(UserManager):
    def _create_user(self, email: str, password: str, **extra_fields: dict) -> User:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()  # user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email: str, password: str, **extra_fields: dict) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class Permission(PermissionsMixin):
    is_superuser = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)


class User(AbstractBaseUser, Permission):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = Manager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
