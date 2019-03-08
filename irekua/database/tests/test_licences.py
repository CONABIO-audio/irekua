from django.test import TestCase

from database.models import Licence

from .test_licence_types import create_simple_licence_type
from . import sample


def create_simple_licence():
    licence_type = create_simple_licence_type()
    metadata = sample.VALID_INSTANCE

    licence = Licence.objects.create(
        licence_type=licence_type,
        metadata=metadata)

    return licence


class LicenceTestCase(TestCase):
    def setUp(self):
        self.licence = create_simple_licence()

    def test_simple_licence_creation(self):
        try:
            create_simple_licence()
        except Exception as e:
            self.fail(e)
