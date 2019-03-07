from django.test import TestCase

from database.models import CollectionUser

from .test_data_collections import create_simple_collection
from .test_users import create_simple_user
from .test_collection_roles import create_simple_collection_role


def create_simple_collection_user():
    collection = create_simple_collection()
    user = create_simple_user()
    collection_role = create_simple_collection_role()

    metadata = {
        "sample_required_parameter": 10
    }

    collection_user, _ = CollectionUser.objects.get_or_create(
        collection=collection,
        user=user,
        defaults=dict(
            role=collection_role.role,
            metadata=metadata,
            is_admin=False)
    )

    return collection_user


class CollectionUserTestCase(TestCase):
    def setUp(self):
        self.colletion_user = create_simple_collection_user()

    def test_simple_collection_user_creation(self):
        try:
            create_simple_collection_user()
        except Exception as e:
            self.fail(e)
