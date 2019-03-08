from django.test import TestCase

from database.models import (
    TermType,
    Schema
)

from . import sample


def create_simple_term_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name=sample.TERM_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.TERM_METADATA,
            description='Sample term metadata schema',
            schema=sample.TERM_METADATA_SCHEMA.schema)
    )

    synonym_metadata_schema, _ = Schema.objects.get_or_create(
        name=sample.SYNONYM_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.SYNONYM_METADATA,
            description='Sample synonym metadata schema',
            schema=sample.SYNONYM_METADATA_SCHEMA.schema)
    )

    term_type, _ = TermType.objects.get_or_create(
        name=sample.TERM_TYPE,
        defaults=dict(
            description='Sample term type',
            is_categorical=True,
            metadata_schema=metadata_schema,
            synonym_metadata_schema=synonym_metadata_schema)
    )

    return term_type


class TermTypeTestCase(TestCase):
    def test_simple_term_type_creation(self):
        try:
            create_simple_term_type()
        except Exception as e:
            self.fail(e)
