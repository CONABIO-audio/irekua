from django.test import TestCase

from database.models import (
    SamplingEventType,
    Schema
)

from . import sample


def create_simple_sampling_event_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name=sample.SAMPLING_EVENT_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.SAMPLING_EVENT_METADATA,
            description='Sample sampling event metadata schema',
            schema=sample.SAMPLING_EVENT_METADATA_SCHEMA.schema)
    )

    sampling_event_type, _ = SamplingEventType.objects.get_or_create(
        name=sample.SAMPLING_EVENT_TYPE,
        defaults=dict(
            description='Sample sampling event type',
            metadata_schema=metadata_schema,
            restrict_site_types=False,
            restrict_device_types=False)
    )

    return sampling_event_type


class SamplingEventTypeTestCase(TestCase):
    def test_simple_sampling_event_type_creation(self):
        try:
            create_simple_sampling_event_type()
        except Exception as e:
            self.fail(e)
