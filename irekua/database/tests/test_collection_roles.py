from django.test import TestCase

# Create your tests here.
from database.models import (
    CollectionRole,
    Schema
)

from .test_collection_types import create_simple_collection_type
from .test_roles import create_simple_role


SAMPLE_COLLECTION_ROLE_METADATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Collection Role Type Metadata Schema",
    "required": [
        "sample_required_parameter"
        ],
    "properties": {
        "sample_parameter": {
            "type": "string",
        },
        "sample_required_parameter": {
            "type": "integer",
        }
    }
}

def create_simple_collection_role():
    collection_type = create_simple_collection_type()
    role = create_simple_role()

    metadata_schema, _ = Schema.objects.get_or_create(
        name='Sample Collection Role Type Metadata Schema',
        defaults=dict(
            field=Schema.COLLECTION_USER_METADATA,
            description='Sample collection role type metadata schema',
            schema=SAMPLE_COLLECTION_ROLE_METADATA_SCHEMA)
    )

    collection_role_type, _ = CollectionRole.objects.get_or_create(
        collection_type=collection_type,
        role=role,
        defaults=dict(metadata_schema=metadata_schema)
    )

    return collection_role_type


class CollectionRoleTestCase(TestCase):
    def setUp(self):
        self.collection_role_type = create_simple_collection_role()

    def test_simple_collection_role_type_creation(self):
        try:
            create_simple_collection_role()
        except:
            self.fail()
