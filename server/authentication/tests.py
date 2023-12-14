from django.contrib.auth import authenticate, get_user_model

import pytest
from authentication.models import User
from faker import Faker

fake = Faker()

USER = {
    "email": fake.email(),
    "password": fake.password(),
}


@pytest.mark.django_db
def test_user_model(django_user_model):
    user = get_user_model()
    assert user == User
    assert django_user_model == User


@pytest.mark.django_db
def test_create_superuser(django_user_model):
    django_user_model.objects.create_superuser(**USER)

    user = authenticate(**USER)
    assert user.is_superuser
    assert user.is_staff
    assert user.is_active
    assert user.role == User.Role.USER


@pytest.mark.django_db
def test_crate_user(django_user_model):
    django_user_model.objects.create_user(**USER, role=User.Role.ADMIN)

    user = authenticate(**USER)
    assert not user.is_superuser
    assert not user.is_staff
    assert user.is_active
    assert user.role == User.Role.ADMIN
