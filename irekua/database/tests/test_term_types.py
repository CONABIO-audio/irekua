from django.test import TestCase

from database.models import TermType

from . import sample


def create_simple_term_type(term_type_name=None):
    if term_type_name is None:
        term_type_name = sample.TERM_TYPE

    term_type, _ = TermType.objects.get_or_create(
        name=term_type_name,
        defaults=dict(
            description='Sample term type',
            is_categorical=True,
            metadata_schema=sample.SCHEMA,
            synonym_metadata_schema=sample.SCHEMA)
    )

    return term_type


class TermTypeTestCase(TestCase):
    def test_simple_term_type_creation(self):
        try:
            create_simple_term_type()
        except Exception as e:
            self.fail(e)
