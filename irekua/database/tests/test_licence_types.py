from django.test import TestCase

from database.models import (
    LicenceType,
    Schema
)


SAMPLE_LICENCE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Licence Metadata Schema",
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


def create_simple_licence_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Licence Metadata Schema',
        defaults=dict(
            field=Schema.LICENCE_METADATA,
            description='Sample licence metadata schema',
            schema=SAMPLE_LICENCE_METADATA_SCHEMA)
    )

    licence_type, _ = LicenceType.objects.get_or_create(
        name='Sample Licence Type',
        defaults=dict(
            description='Sample licence type',
            metadata_schema=metadata_schema,
            can_view=True,
            can_download=True,
            can_view_annotations=True,
            can_annotate=True,
            can_vote_annotations=True)
    )

    return licence_type


class LicenceTypeTestCase(TestCase):
    def setUp(self):
        self.licence_type = create_simple_licence_type()

    def test_simple_licence_type_creation(self):
        try:
            create_simple_licence_type()
        except Exception as e:
            self.fail(e)
