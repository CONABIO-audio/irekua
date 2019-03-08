from django.test import TestCase

from database.models import Schema

from . import sample


def create_simple_schema():
    schema, _ = Schema.objects.get_or_create(
        name=sample.SCHEMA['title'],
        field=Schema.GLOBAL,
        description='Sample schema',
        schema=sample.SCHEMA)
    return schema


class SchemaTestCase(TestCase):
    def test_simple_schema_creation(self):
        try:
            create_simple_schema()
        except Exception as e:
            self.fail(e)
