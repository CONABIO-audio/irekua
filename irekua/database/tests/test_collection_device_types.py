from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import CollectionDeviceType

from .test_device_types import create_simple_device_type
from .test_collection_types import create_simple_collection_type
from . import sample


def create_simple_collection_device_type():
    device_type = create_simple_device_type()
    collection_type = create_simple_collection_type()

    collection_device_type, _ = CollectionDeviceType.objects.get_or_create(
        collection_type=collection_type,
        device_type=device_type,
        defaults=dict(
            metadata_schema=sample.SCHEMA)
    )

    return collection_device_type


class CollectionDeviceTypeTestCase(TestCase):
    def test_simple_collection_device_type_creation(self):
        try:
            create_simple_collection_device_type()
        except Exception as e:
            self.fail(e)

    def test_validate_metadata(self):
        pass
