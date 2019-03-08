from django.test import TestCase

from database.models import MetaCollection

from .test_users import create_simple_user
from . import sample


def create_simple_metacollection():
    user = create_simple_user()

    metacollection, _ = MetaCollection.objects.get_or_create(
        name=sample.METACOLLECTION,
        description='Sample meta collection',
        creator=user)

    return metacollection


class MetaCollectionTestCase(TestCase):
    def test_simple_metacollection_creation(self):
        try:
            create_simple_metacollection()
        except Exception as e:
            self.fail(e)
