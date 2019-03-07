from django.test import TestCase

# Create your tests here.
from database.models import (
    CollectionItemType,
    Schema
)

from .test_collection_types import create_simple_collection_type
from .test_item_types import create_simple_item_type


SAMPLE_COLLECTION_ITEM_TYPE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Collection Item Type Metadata Schema",
    "required": [
        "sample_required_parameter"
        ],
    "properties": {
        "sample_parameter": {
            "type": "string",
        },
        "sample_required_parameter": {
            "type": "integer",
        }
    }
}

def create_simple_collection_item_type():
    collection_type = create_simple_collection_type()
    item_type = create_simple_item_type()

    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Item Type Metadata Schema',
        defaults=dict(
            field=Schema.ITEM_METADATA,
            description='Sample item type metadata schema',
            schema=SAMPLE_COLLECTION_ITEM_TYPE_METADATA_SCHEMA)
    )

    collection_item_type, _ = CollectionItemType.objects.get_or_create(
        collection_type=collection_type,
        item_type=item_type,
        defaults=dict(metadata_schema=metadata_schema)
    )

    return collection_item_type


class CollectionItemTypeTestCase(TestCase):
    def setUp(self):
        self.collection_item_type = create_simple_collection_item_type()

    def test_simple_collection_item_type_creation(self):
        try:
            create_simple_collection_item_type()
        except:
            self.fail()
