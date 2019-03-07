from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import (
    CollectionDeviceType,
    Schema
)

from .test_device_types import create_simple_device_type
from .test_collection_types import create_simple_collection_type


SAMPLE_COLLECTION_DEVICE_TYPE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Device Metadata Schema",
    "required": [
        "was_calibrated",
    ],
    "properties": {
        "was_calibrated": {
            "type": "boolean",
        },
        "maintenance_unit": {
            "type": "string",
        },
    }
}


def create_simple_collection_device_type():
    device_type = create_simple_device_type()
    collection_type = create_simple_collection_type()

    schema, _ = Schema.objects.get_or_create(
        name='Sample Collection Device Metadata',
        defaults=dict(
            field=Schema.COLLECTION_DEVICE_METADATA,
            description='Sample schema for metadata of device of type within collection',
            schema=SAMPLE_COLLECTION_DEVICE_TYPE_METADATA_SCHEMA)
    )

    collection_device_type , _ = CollectionDeviceType.objects.get_or_create(
        collection_type=collection_type,
        device_type=device_type,
        defaults=dict(
            metadata_schema=schema)
    )

    return collection_device_type


class CollectionDeviceTypeTestCase(TestCase):
    def setUp(self):
        self.collection_device_type = create_simple_collection_device_type()

    def test_simple_collection_device_type_creation(self):
        try:
            create_simple_collection_device_type()
        except:
            self.fail()

    def test_validate_metadata(self):
        pass
