from django.test import TestCase

from database.models import Term

from .test_term_types import create_simple_term_type


def create_simple_term():
    term_type = create_simple_term_type()

    metadata = {
        'sample_required_parameter': 10
    }

    term, _ = Term.objects.get_or_create(
        term_type=term_type,
        value='Sample Term Value',
        defaults=dict(
            description='Sample term value',
            metadata=metadata)
    )

    return term


class TermTestCase(TestCase):
    def setUp(self):
        self.term = create_simple_term()

    def test_simple_term_creation(self):
        try:
            create_simple_term()
        except Exception as e:
            self.fail(e)
