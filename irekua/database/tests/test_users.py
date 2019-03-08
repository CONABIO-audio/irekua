from django.test import TestCase

from django.contrib.auth.models import User

from . import sample


def create_simple_user():
    user, _ = User.objects.get_or_create(
        username=sample.USER_NAME,
        defaults=dict(
            password=sample.USER_PASSWORD,
            email=sample.USER_EMAIL,
            first_name=sample.USER_FIRST_NAME,
            is_staff=False,
            is_superuser=False)
    )
    return user


class UserTestCase(TestCase):
    pass
