from django.test import TestCase

from database.models import SamplingEventType

from . import sample


def create_simple_sampling_event_type():
    sampling_event_type, _ = SamplingEventType.objects.get_or_create(
        name=sample.SAMPLING_EVENT_TYPE,
        defaults=dict(
            description='Sample sampling event type',
            metadata_schema=sample.SCHEMA,
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
