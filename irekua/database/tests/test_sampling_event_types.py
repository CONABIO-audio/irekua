from django.test import TestCase

from database.models import (
    SamplingEventType,
    Schema
)


SAMPLE_SAMPLING_EVENT_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Sampling Event Metadata Schema",
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


def create_simple_sampling_event_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Sampling Event Metadata Schema',
        defaults=dict(
            field=Schema.SAMPLING_EVENT_METADATA,
            description='Sample sampling event metadata schema',
            schema=SAMPLE_SAMPLING_EVENT_METADATA_SCHEMA)
    )

    sampling_event, _ = SamplingEventType.objects.get_or_create(
        name='Sample Sampling Event Type',
        defaults=dict(
            description='Sample sampling event type',
            metadata_schema=metadata_schema,
            restrict_site_types=False,
            restrict_device_types=False)
    )

    return sampling_event


class SamplingEventTypeTestCase(TestCase):
    def setUp(self):
        self.sampling_event_type = create_simple_sampling_event_type()

    def test_simple_sampling_event_type_creation(self):
        try:
            create_simple_sampling_event_type()
        except Exception as e:
            self.fail(e)
