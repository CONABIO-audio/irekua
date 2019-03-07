from django.test import TestCase

from database.models import Source

from .test_users import create_simple_user


def create_simple_source():
    user = create_simple_user()

    source, _ = Source.objects.get_or_create(
        directory='/sample/source/directory/',
        defaults=dict(
            source_file='sample_source_file.csv',
            parse_function='sample_parse_function',
            uploader=user)
    )

    return source


class SourceTestCase(TestCase):
    def setUp(self):
        self.source = create_simple_source()

    def test_simple_source_creation(self):
        try:
            create_simple_source()
        except Exception as e:
            self.fail(e)
