from django.test import TestCase

from database.models import (
    TermType,
    Schema
)


SAMPLE_TERM_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Collection Item Type Metadata Schema",
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

SAMPLE_TERM_SYNONYM_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Collection Item Type Metadata Schema",
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


def create_simple_term_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Term Metadata Schema',
        defaults=dict(
            field=Schema.TERM_METADATA,
            description='Sample term metadata schema',
            schema=SAMPLE_TERM_METADATA_SCHEMA)
    )

    synonym_metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Synonym Metadata Schema',
        defaults=dict(
            field=Schema.SYNONYM_METADATA,
            description='Sample synonym metadata schema',
            schema=SAMPLE_TERM_SYNONYM_METADATA_SCHEMA)
    )

    term_type, _ = TermType.objects.get_or_create(
        name='Sample Term Type',
        defaults=dict(
            description='Sample term type',
            is_categorical=True,
            metadata_schema=metadata_schema,
            synonym_metadata_schema=synonym_metadata_schema)
    )

    return term_type


class TermTypeTestCase(TestCase):
    def setUp(self):
        self.term_type = create_simple_term_type()

    def test_simple_term_type_creation(self):
        try:
            create_simple_term_type()
        except Exception as e:
            self.fail(e)
