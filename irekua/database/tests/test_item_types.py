from django.test import TestCase

from database.models import ItemType

from .test_event_types import create_simple_event_type
from . import sample


def create_simple_item_type():
    item_type, _ = ItemType.objects.get_or_create(
        name=sample.ITEM_TYPE,
        defaults=dict(
            description='Sample item type',
            media_info_schema=sample.SCHEMA,
            media_type=sample.ITEM_MIME)
    )

    event_type = create_simple_event_type()
    item_type.event_types.add(event_type)

    return item_type


class ItemTypeTestCase(TestCase):
    def test_simple_item_type_creation(self):
        try:
            create_simple_item_type()
        except Exception as e:
            self.fail(e)
