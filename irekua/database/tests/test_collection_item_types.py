from django.test import TestCase

# Create your tests here.
from database.models import CollectionItemType

from .test_collection_types import create_simple_collection_type
from .test_item_types import create_simple_item_type
from . import sample


def create_simple_collection_item_type():
    collection_type = create_simple_collection_type()
    item_type = create_simple_item_type()

    collection_item_type, _ = CollectionItemType.objects.get_or_create(
        collection_type=collection_type,
        item_type=item_type,
        defaults=dict(metadata_schema=sample.SCHEMA)
    )

    return collection_item_type


class CollectionItemTypeTestCase(TestCase):
    def test_simple_collection_item_type_creation(self):
        try:
            create_simple_collection_item_type()
        except Exception as e:
            self.fail(e)
