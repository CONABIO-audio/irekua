from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import (
    CollectionType,
    Schema
)

from . import sample


def create_simple_collection_type():
    schema, _ = Schema.objects.get_or_create(
        name=sample.COLLECTION_TYPE_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.COLLECTION_METADATA,
            description='Sample collection type schema',
            schema=sample.COLLECTION_TYPE_METADATA_SCHEMA.schema)
    )

    collection_type, _ = CollectionType.objects.get_or_create(
        name=sample.COLLECTION_TYPE,
        defaults=dict(
            description='Sample collection type',
            metadata_schema=schema,
            restrict_site_types=False,
            restrict_annotation_types=False,
            restrict_item_types=False,
            restrict_licence_types=False,
            restrict_device_types=False,
            restrict_event_types=False,
            restrict_sampling_event_types=False)
    )

    return collection_type


class CollectionTypeTestCase(TestCase):
    def test_creation_simple_collection_type(self):
        try:
            create_simple_collection_type()
        except Exception as e:
            self.fail(e)
