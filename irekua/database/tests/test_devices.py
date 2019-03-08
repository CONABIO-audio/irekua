from django.test import TestCase

from database.models import (
    Device,
    Schema
)

from .test_device_types import create_simple_device_type
from .test_device_brands import create_simple_device_brand
from . import sample


def create_simple_device():
    device_type = create_simple_device_type()
    brand = create_simple_device_brand()

    metadata_schema, _ = Schema.objects.get_or_create(
        name=sample.DEVICE_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.DEVICE_METADATA,
            description='Sample device metadata schema',
            schema=sample.DEVICE_METADATA_SCHEMA.schema)
    )

    configuration_schema, _ = Schema.objects.get_or_create(
        name=sample.DEVICE_CONFIGURATION_SCHEMA.name,
        defaults=dict(
            field=Schema.DEVICE_CONFIGURATION,
            description='Sample device configuration schema',
            schema=sample.DEVICE_CONFIGURATION_SCHEMA.schema)
    )

    device, _ = Device.objects.get_or_create(
        device_type=device_type,
        brand=brand,
        model=sample.DEVICE_MODEL,
        defaults=dict(
            metadata_schema=metadata_schema,
            configuration_schema=configuration_schema)
    )

    return device


class DeviceTestCase(TestCase):
    def test_simple_device_creation(self):
        try:
            create_simple_device()
        except Exception as e:
            self.fail(e)
