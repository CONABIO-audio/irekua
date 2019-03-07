from django.test import TestCase

# Create your tests here.
from database.models import UserData
from django.contrib.auth.models import User


def create_simple_user():
    user, _  = User.objects.get_or_create(
        username='sampleuser',
        defaults=dict(
            password='sampleuser',
            email='sampleuser@sample.domain.com',
            first_name='Sample User',
            is_staff=False,
            is_superuser=False)
    )
    return user


class UserTestCase(TestCase):
    pass
