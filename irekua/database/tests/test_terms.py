from django.test import TestCase

from database.models import Term

from .test_term_types import create_simple_term_type
from . import sample


def create_simple_term():
    term_type = create_simple_term_type()
    metadata = sample.VALID_INSTANCE

    term, _ = Term.objects.get_or_create(
        term_type=term_type,
        value=sample.TERM_VALUE,
        defaults=dict(
            description='Sample term value',
            metadata=metadata)
    )

    return term


class TermTestCase(TestCase):
    def test_simple_term_creation(self):
        try:
            create_simple_term()
        except Exception as e:
            self.fail(e)
