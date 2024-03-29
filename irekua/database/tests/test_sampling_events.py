from django.test import TestCase

from database.models import SamplingEvent

from .test_sampling_event_types import create_simple_sampling_event_type
from .test_physical_devices import create_simple_physical_device
from .test_sites import create_simple_site
from .test_data_collections import create_simple_collection
from .test_users import create_simple_user
from .test_licences import create_simple_licence
from . import sample


def create_simple_sampling_event():
    sampling_event_type = create_simple_sampling_event_type()
    device = create_simple_physical_device()
    site = create_simple_site()
    collection = create_simple_collection()
    licence = create_simple_licence(collection=collection)
    user = create_simple_user()
    metadata = sample.VALID_INSTANCE
    configuration = sample.VALID_INSTANCE

    sampling_event = SamplingEvent.objects.create(
        sampling_event_type=sampling_event_type,
        device=device,
        configuration=configuration,
        licence=licence,
        metadata=metadata,
        collection=collection,
        created_by=user,
        site=site)

    return sampling_event


class SamplingEvenTestCase(TestCase):
    def test_simple_sampling_event_creation(self):
        try:
            create_simple_sampling_event()
        except Exception as e:
            self.fail(e)
