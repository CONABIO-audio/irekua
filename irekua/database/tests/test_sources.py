from django.test import TestCase

from database.models import Source

from .test_users import create_simple_user
from . import sample


def create_simple_source():
    user = create_simple_user()

    source, _ = Source.objects.get_or_create(
        directory=sample.SOURCE_DIRECTORY,
        defaults=dict(
            source_file=sample.SOURCE_FILE,
            parse_function=sample.PARSE_FUNCTION,
            uploader=user)
    )

    return source


class SourceTestCase(TestCase):
    def test_simple_source_creation(self):
        try:
            create_simple_source()
        except Exception as e:
            self.fail(e)
