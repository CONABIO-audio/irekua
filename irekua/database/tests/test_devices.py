from django.test import TestCase

from database.models import (
    Device,
    Schema
)

from .test_device_types import create_simple_device_type
from .test_device_brands import create_simple_device_brand


SAMPLE_DEVICE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Device Metadata Schema",
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

SAMPLE_DEVICE_CONFIGURATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Device Metadata Schema",
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


def create_simple_device():
    device_type = create_simple_device_type()
    brand = create_simple_device_brand()

    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Device Metadata Schema',
        defaults=dict(
            field=Schema.DEVICE_METADATA,
            description='Sample device metadata schema',
            schema=SAMPLE_DEVICE_METADATA_SCHEMA)
    )

    configuration_schema, _ = Schema.objects.get_or_create(
        name='Sample Device Configuration Schema',
        defaults=dict(
            field=Schema.DEVICE_CONFIGURATION,
            description='Sample device configuration schema',
            schema=SAMPLE_DEVICE_CONFIGURATION_SCHEMA)
    )

    device, _ = Device.objects.get_or_create(
        device_type=device_type,
        brand=brand,
        model='Sample Model',
        defaults=dict(
            metadata_schema=metadata_schema,
            configuration_schema=configuration_schema)
    )

    return device


class DeviceTestCase(TestCase):
    def setUp(self):
        self.device = create_simple_device()

    def test_simple_device_creation(self):
        try:
            create_simple_device()
        except Exception as e:
            self.fail(e)
