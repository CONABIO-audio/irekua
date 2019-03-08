from django.test import TestCase
from django.core.exceptions import ValidationError

from database.models import Institution

from . import sample


def create_simple_institution():
    institution, _ = Institution.objects.get_or_create(
        institution_name=sample.INSTITUTION)
    return institution


class InstitutionTestCase(TestCase):
    def test_simple_institution_creation(self):
        try:
            create_simple_institution()
        except Exception as e:
            self.fail(e)
