from rest_framework.test import APITestCase
from uuid import uuid4

from django.contrib.auth.models import User
from database.models import UserData

from database.tests.test_data_collections import create_simple_collection
from database.tests.test_collection_roles import create_simple_role


def create_or_get_user(
        is_staff=None,
        is_superuser=None,
        is_developer=None,
        is_curator=None,
        is_model=None):

    user, _ = User.objects.get_or_create(
        username=uuid4(),
        defaults=dict(
            password=uuid4(),
            is_staff=is_staff,
            is_superuser=is_superuser)
    )

    UserData.objects.get_or_create(
        user=user,
        defaults=dict(
            is_developer=is_developer,
            is_curator=is_curator,
            is_model=is_model)
    )

    return user

class BaseTestCase(APITestCase):
    def setUp(self):
        self.admin_user = create_or_get_user(
            is_superuser=True,
            is_staff=True,
            is_developer=False,
            is_curator=False,
            is_model=False)

        self.regular_user = create_or_get_user(
            is_superuser=False,
            is_staff=False,
            is_developer=False,
            is_curator=False,
            is_model=False)

        self.model_user = create_or_get_user(
            is_superuser=False,
            is_staff=False,
            is_developer=False,
            is_curator=False,
            is_model=True)

        self.developer_user = create_or_get_user(
            is_superuser=False,
            is_staff=False,
            is_developer=True,
            is_curator=False,
            is_model=False)

        self.curator_user = create_or_get_user(
            is_superuser=False,
            is_staff=False,
            is_developer=False,
            is_curator=True,
            is_model=False)

        self.collection = create_simple_collection()
        self.role = create_simple_role()
        self.collection.collection_type.add_role(self.role)

        self.collection_user = create_or_get_user(
            is_superuser=False,
            is_staff=False,
            is_developer=False,
            is_curator=False,
            is_model=False)

        self.collection.add_user(self.collection_user, role=self.role, metadata={})
