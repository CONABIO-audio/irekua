from django.test import TestCase

from database.models import Item


from .test_item_types import create_simple_item_type
from .test_sampling_events import create_simple_sampling_event
from .test_sources import create_simple_source
from . import sample


def create_simple_item():
    item_type = create_simple_item_type()
    sampling_event = create_simple_sampling_event()
    source = create_simple_source()

    metadata = sample.VALID_INSTANCE
    media_info = sample.VALID_INSTANCE

    item, _ = Item.objects.get_or_create(
        hash=sample.ITEM_HASH,
        defaults=dict(
            filesize=100000,
            item_type=item_type,
            media_info=media_info,
            sampling_event=sampling_event,
            source=source,
            metadata=metadata)
    )

    return item


class ItemTestCase(TestCase):
    def test_simple_item_creation(self):
        try:
            create_simple_item()
        except Exception as e:
            self.fail(e)
