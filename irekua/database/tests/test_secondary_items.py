from django.test import TestCase

from database.models import SecondaryItem

from .test_item_types import create_simple_item_type
from .test_items import create_simple_item


def create_simple_secondary_item():
    item_type = create_simple_item_type()
    item = create_simple_item()

    media_info = {
        'sample_required_parameter': 110
    }

    secondary_item, _ = SecondaryItem.objects.get_or_create(
        path='/sample/path/to/secondary/item.wav',
        hash='samplehashofsecondaryitem',
        defaults=dict(
            hash_function='md5',
            item_type=item_type,
            item=item,
            media_info=media_info)
    )

    return secondary_item


class SecondaryItemTestCase(TestCase):
    def setUp(self):
        self.secondary_item = create_simple_secondary_item()

    def test_simple_secondary_item_creation(self):
        try:
            create_simple_secondary_item()
        except Exception as e:
            self.fail(e)
