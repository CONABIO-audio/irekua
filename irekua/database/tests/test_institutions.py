from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import Institution


def create_simple_institution():
    institution, _ = Institution.objects.get_or_create(
        institution_name='Sample Institution',
        institution_code='SI',
        subdependency='Sample Subdependency')
    return institution


class InstitutionTestCase(TestCase):
    def setUp(self):
        self.institution = create_simple_institution()

    def test_simple_institution_creation(self):
        try:
            create_simple_institution()
        except:
            self.fail('Intitution creation failed')
