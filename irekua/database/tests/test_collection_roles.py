from django.test import TestCase

# Create your tests here.
from database.models import CollectionRole

from .test_collection_types import create_simple_collection_type
from .test_roles import create_simple_role
from . import sample


def create_simple_collection_role():
    collection_type = create_simple_collection_type()
    role = create_simple_role()

    collection_role_type, _ = CollectionRole.objects.get_or_create(
        collection_type=collection_type,
        role=role,
        defaults=dict(metadata_schema=sample.SCHEMA)
    )

    return collection_role_type


class CollectionRoleTestCase(TestCase):
    def test_simple_collection_role_type_creation(self):
        try:
            create_simple_collection_role()
        except Exception as e:
            self.fail(e)
