from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import Collection

from .test_collection_types import create_simple_collection_type
from .test_institutions import create_simple_institution

from . import sample


def create_simple_collection():
    collection_type = create_simple_collection_type()
    institution = create_simple_institution()
    metadata = sample.VALID_INSTANCE

    collection, _ = Collection.objects.get_or_create(
        name=sample.COLLECTION,
        defaults=dict(
            collection_type=collection_type,
            description='Sample collection',
            metadata=metadata,
            institution=institution)
    )

    return collection


class CollectionTestCase(TestCase):
    def test_simple_collection_creation(self):
        try:
            create_simple_collection()
        except Exception as e:
            self.fail(e)
