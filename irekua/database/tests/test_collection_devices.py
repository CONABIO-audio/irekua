from django.test import TestCase

# Create your tests here.
from database.models import CollectionDevice

from .test_physical_devices import create_simple_physical_device
from .test_data_collections import create_simple_collection


def create_simple_collection_device():
    device = create_simple_physical_device()
    collection = create_simple_collection()

    metadata = {
        'was_calibrated': True
    }

    collection_device, _ = CollectionDevice.objects.get_or_create(
        collection=collection,
        internal_id='123456789',
        defaults=dict(
            device=device,
            metadata=metadata)
    )

    return collection_device


class CollectionDeviceTestCase(TestCase):
    def setUp(self):
        self.collection_device = create_simple_collection_device()

    def test_simple_collection_device_creation(self):
        try:
            create_simple_collection_device()
        except:
            self.fail()
