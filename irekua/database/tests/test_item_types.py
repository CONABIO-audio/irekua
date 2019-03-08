from django.test import TestCase

from database.models import (
    ItemType,
    Schema
)

from .test_event_types import create_simple_event_type
from . import sample


def create_simple_item_type():
    media_info_schema, _ = Schema.objects.get_or_create(
        name=sample.MEDIA_INFO_SCHEMA.name,
        defaults=dict(
            field=Schema.ITEM_MEDIA_INFO,
            description='Sample item media info schema',
            schema=sample.MEDIA_INFO_SCHEMA.schema)
    )

    item_type, _ = ItemType.objects.get_or_create(
        name=sample.ITEM_TYPE,
        defaults=dict(
            description='Sample item type',
            media_info_schema=media_info_schema,
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
