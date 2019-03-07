from django.test import TestCase

from database.models import (
    SiteType,
    Schema
)


SAMPLE_SITE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Site Metadata Schema",
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

def create_simple_site_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Site Metadata Schema',
        defaults=dict(
            field=Schema.SITE_METADATA,
            description='Sample site metadata schema',
            schema=SAMPLE_SITE_METADATA_SCHEMA)
    )

    site_type, _ = SiteType.objects.get_or_create(
        name='Sample Site Type',
        defaults=dict(
            description='Sample site type',
            metadata_schema=metadata_schema)
    )

    return site_type


class SiteTypeTestCase(TestCase):
    def setUp(self):
        self.site_type = create_simple_site_type()

    def test_simple_site_type_creation(self):
        try:
            create_simple_site_type()
        except:
            self.fail()
