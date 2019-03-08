from django.test import TestCase

from database.models import (
    SiteType,
    Schema
)

from . import sample


def create_simple_site_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name=sample.SITE_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.SITE_METADATA,
            description='Sample site metadata schema',
            schema=sample.SITE_METADATA_SCHEMA.schema)
    )

    site_type, _ = SiteType.objects.get_or_create(
        name=sample.SITE_TYPE,
        defaults=dict(
            description='Sample site type',
            metadata_schema=metadata_schema)
    )

    return site_type


class SiteTypeTestCase(TestCase):
    def test_simple_site_type_creation(self):
        try:
            create_simple_site_type()
        except Exception as e:
            self.fail(e)
