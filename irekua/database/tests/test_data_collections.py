from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import Collection

from .test_collection_types import create_simple_collection_type
from .test_institutions import create_simple_institution


def create_simple_collection():
    collection_type = create_simple_collection_type()
    institution = create_simple_institution()

    metadata = {
        'contract_number': 5673284,
        'subcollection_manager': 'sample_manager'
    }

    collection, _ = Collection.objects.get_or_create(
        collection_type=collection_type,
        name='Sample Collection',
        description='Sample collection',
        metadata=metadata,
        institution=institution,
        is_open=True)

    return collection


class CollectionTestCase(TestCase):
    def setUp(self):
        self.collection = create_simple_collection()

    def test_simple_collection_creation(self):
        try:
            create_simple_collection()
        except:
            self.fail('Collection creation failed')
