from django.test import TestCase

from database.models import (
    ItemType,
    Schema
)

from .test_event_types import create_simple_event_type


SAMPLE_MEDIA_INFO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Item Media Info Schema",
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


def create_simple_item_type():
    media_info_schema, _ = Schema.objects.get_or_create(
        name='Sample Item Media Info Schema',
        defaults=dict(
            field=Schema.ITEM_MEDIA_INFO,
            description='Sample item media info schema',
            schema=SAMPLE_MEDIA_INFO_SCHEMA)
    )

    item_type, _ = ItemType.objects.get_or_create(
        name='Sample Item Type',
        defaults=dict(
            description='Sample item type',
            media_info_schema=media_info_schema,
            media_type='audio/x-wav')
    )

    event_type = create_simple_event_type()
    item_type.event_types.add(event_type)

    return item_type


class ItemTypeTestCase(TestCase):
    def setUp(self):
        self.item_type = create_simple_item_type()

    def test_simple_item_type_creation(self):
        try:
            create_simple_item_type()
        except Exception as e:
            self.fail(e)
