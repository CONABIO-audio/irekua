from django.test import TestCase

from database.models import Entailment

from .test_term_types import create_simple_term_type
from .test_entailment_types import create_simple_entailment_type
from .test_terms import create_simple_term
from . import sample


def create_simple_entailment():
    source = create_simple_term()
    metadata = sample.VALID_INSTANCE

    target_type = create_simple_term_type(sample.ENTAILMENT_TARGET_TYPE)
    target = create_simple_term(target_type)

    create_simple_entailment_type()

    entailment, _ = Entailment.objects.get_or_create(
        source=source,
        target=target,
        metadata=metadata)

    return entailment


class EntailmentTestCase(TestCase):
    def test_simple_entailment_creation(self):
        try:
            create_simple_entailment()
        except Exception as e:
            self.fail(e)
