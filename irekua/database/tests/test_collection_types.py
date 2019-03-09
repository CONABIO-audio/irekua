from django.test import TestCase
from django.core.exceptions import ValidationError

from database.models import CollectionType
from . import sample


def create_simple_collection_type():
    collection_type, _ = CollectionType.objects.get_or_create(
        name=sample.COLLECTION_TYPE,
        defaults=dict(
            description='Sample collection type',
            metadata_schema=sample.SCHEMA,
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
