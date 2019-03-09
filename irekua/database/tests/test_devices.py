from django.test import TestCase

from database.models import Device

from .test_device_types import create_simple_device_type
from .test_device_brands import create_simple_device_brand
from . import sample


def create_simple_device():
    device_type = create_simple_device_type()
    brand = create_simple_device_brand()

    device, _ = Device.objects.get_or_create(
        device_type=device_type,
        brand=brand,
        model=sample.DEVICE_MODEL,
        defaults=dict(
            metadata_schema=sample.SCHEMA,
            configuration_schema=sample.SCHEMA)
    )

    return device


class DeviceTestCase(TestCase):
    def test_simple_device_creation(self):
        try:
            create_simple_device()
        except Exception as e:
            self.fail(e)
