from django.test import TestCase

# Create your tests here.
from database.models import CollectionSite

from .test_sites import create_simple_site
from .test_data_collections import create_simple_collection
from . import sample


def create_simple_collection_site():
    site = create_simple_site()
    collection = create_simple_collection()
    metadata = sample.VALID_INSTANCE

    collection_site, _ = CollectionSite.objects.get_or_create(
        collection=collection,
        internal_id='123456789',
        defaults=dict(
            site=site,
            metadata=metadata)
    )

    return collection_site


class CollectionSiteTestCase(TestCase):
    def test_simple_collection_site_creation(self):
        try:
            create_simple_collection_site()
        except Exception as e:
            self.fail(e)
