from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import (
    CollectionType,
    Schema
)


SAMPLE_COLLECTION_TYPE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Collection Type Metadata",
    "required": [
        "contract_number",
        "subcollection_manager",
    ],
    "properties": {
        "contract_number": {
            "type": "integer",
        },
        "subcollection_manager": {
            "type": "string",
        },
        "valid_years": {
            "type": "string",
        }
    }
}


def create_simple_collection_type():
    schema, _ = Schema.objects.get_or_create(
        field=Schema.COLLECTION_METADATA,
        name='Sample Collection Type Schema',
        description='Sample collection type schema',
        schema=SAMPLE_COLLECTION_TYPE_METADATA_SCHEMA)

    collection_type, _ = CollectionType.objects.get_or_create(
        name='Sample Collection Type',
        description='Sample collection type',
        metadata_schema=schema,
        restrict_site_types=False,
        restrict_annotation_types=False,
        restrict_item_types=False,
        restrict_licence_types=False,
        restrict_device_types=False,
        restrict_event_types=False,
        restrict_sampling_event_types=False)

    return collection_type


class CollectionTypeTestCase(TestCase):
    def setUp(self):
        self.collection_type = create_simple_collection_type()

    def test_creation_simple_collection_type(self):
        try:
            create_simple_collection_type()
        except:
            self.fail('Creation of collection type failed')
