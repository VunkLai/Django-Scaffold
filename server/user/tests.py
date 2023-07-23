from django.contrib.auth import get_user_model

from user.models import User


def test_user_model():
    user = get_user_model()
    assert user == User
