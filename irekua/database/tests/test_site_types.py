from django.test import TestCase

from database.models import SiteType
from . import sample


def create_simple_site_type():
    site_type, _ = SiteType.objects.get_or_create(
        name=sample.SITE_TYPE,
        defaults=dict(
            description='Sample site type',
            metadata_schema=sample.SCHEMA)
    )

    return site_type


class SiteTypeTestCase(TestCase):
    def test_simple_site_type_creation(self):
        try:
            create_simple_site_type()
        except Exception as e:
            self.fail(e)
