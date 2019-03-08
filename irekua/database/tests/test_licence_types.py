from django.test import TestCase

from database.models import (
    LicenceType,
    Schema
)

from . import sample


def create_simple_licence_type():
    metadata_schema, _ = Schema.objects.get_or_create(
        name=sample.LICENCE_METADATA_SCHEMA.name,
        defaults=dict(
            field=Schema.LICENCE_METADATA,
            description='Sample licence metadata schema',
            schema=sample.LICENCE_METADATA_SCHEMA.schema)
    )

    licence_type, _ = LicenceType.objects.get_or_create(
        name=sample.LICENCE_TYPE,
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
    def test_simple_licence_type_creation(self):
        try:
            create_simple_licence_type()
        except Exception as e:
            self.fail(e)
