from django.test import TestCase

from database.models import SamplingEvent

from .test_sampling_event_types import create_simple_sampling_event_type
from .test_physical_devices import create_simple_physical_device
from .test_sites import create_simple_site


def create_simple_sampling_event():
    sampling_event_type = create_simple_sampling_event_type()
    device = create_simple_physical_device()
    site = create_simple_site()

    metadata = {
        'sample_required_parameter': 90
    }

    configuration = {
        'sample_required_parameter': 100
    }

    sampling_event = SamplingEvent.objects.create(
        sampling_event_type=sampling_event_type,
        device=device,
        configuration=configuration,
        metadata=metadata,
        site=site)

    return sampling_event


class SamplingEvenTestCase(TestCase):
    def setUp(self):
        self.sampling_event = create_simple_sampling_event()

    def test_simple_sampling_event_creation(self):
        try:
            create_simple_sampling_event()
        except Exception as e:
            self.fail(e)
