from django.test import TestCase

from database.models import EntailmentType

from .test_term_types import create_simple_term_type
from . import sample


def create_simple_entailment_type():
    source_type = create_simple_term_type()
    target_type = create_simple_term_type(sample.ENTAILMENT_TARGET_TYPE)

    entailment_type, _ = EntailmentType.objects.get_or_create(
        source_type=source_type,
        target_type=target_type,
        metadata_schema=sample.SCHEMA)

    return entailment_type


class EntailmentTypeTestCase(TestCase):
    def test_simple_entailment_type_creation(self):
        try:
            create_simple_entailment_type()
        except Exception as e:
            self.fail(e)
