from django.test import TestCase

from database.models import Item


from .test_item_types import create_simple_item_type
from .test_sampling_events import create_simple_sampling_event
from .test_sources import create_simple_source
from .test_data_collections import create_simple_collection
from .test_users import create_simple_user
from .test_licences import create_simple_licence


def create_simple_item():
    item_type = create_simple_item_type()
    sampling_event = create_simple_sampling_event()
    source = create_simple_source()
    collection = create_simple_collection()
    user = create_simple_user()
    licence = create_simple_licence()

    collection.add_licence(licence)

    metadata = {
        'sample_required_parameter': 40
    }

    media_info = {
        'sample_required_parameter': 50
    }

    item, _ = Item.objects.get_or_create(
        path='/sample/path/to/item.wav',
        hash='samplehash',
        defaults=dict(
            filesize=100000,
            hash_function='md5',
            item_type=item_type,
            media_info=media_info,
            sampling_event=sampling_event,
            source=source,
            metadata=metadata,
            collection=collection,
            owner=user,
            licence=licence,
            is_uploaded=False)
    )

    return item


class ItemTestCase(TestCase):
    def setUp(self):
        self.item = create_simple_item()

    def test_simple_item_creation(self):
        try:
            create_simple_item()
        except Exception as e:
            self.fail(e)
