from django.test import TestCase

from database.models import Schema

SAMPLE_SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": [
        "checked",
        "dimensions",
        "id",
        "name",
        "price",
        "tags"
    ],
    "properties": {
        "checked": {
            "$id": "#/properties/checked",
            "type": "boolean",
            "title": "The Checked Schema",
            "default": False,
            "examples": [
                False
            ]
        },
        "dimensions": {
            "$id": "#/properties/dimensions",
            "type": "object",
            "title": "The Dimensions Schema",
            "required": [
                "width",
                "height"
            ],
            "properties": {
                "width": {
                    "$id": "#/properties/dimensions/properties/width",
                    "type": "integer",
                    "title": "The Width Schema",
                    "default": 0,
                    "examples": [
                        5
                    ]
                },
                "height": {
                    "$id": "#/properties/dimensions/properties/height",
                    "type": "integer",
                    "title": "The Height Schema",
                    "default": 0,
                    "examples": [
                        10
                    ]
                }
            }
        },
        "id": {
            "$id": "#/properties/id",
            "type": "integer",
            "title": "The Id Schema",
            "default": 0,
            "examples": [
                1
            ]
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The Name Schema",
            "default": "",
            "examples": [
                "A green door"
            ],
            "pattern": "^(.*)$"
        },
        "price": {
            "$id": "#/properties/price",
            "type": "number",
            "title": "The Price Schema",
            "default": 0.0,
            "examples": [
                12.5
            ]
        },
        "tags": {
            "$id": "#/properties/tags",
            "type": "array",
            "title": "The Tags Schema",
            "items": {
                "$id": "#/properties/tags/items",
                "type": "string",
                "title": "The Items Schema",
                "default": "",
                "examples": [
                    "home",
                    "green"
                ],
                "pattern": "^(.*)$"
            }
        }
    }
}


def create_simple_schema():
    schema, _ = Schema.objects.get_or_create(
    name='Sample Schema',
    field=Schema.GLOBAL,
    description='Sample schema',
    schema=SAMPLE_SCHEMA)

    return schema


class SchemaTestCase(TestCase):
    def setUp(self):
        self.schema = create_simple_schema()

    def test_simple_schema_creation(self):
        try:
            create_simple_schema()
        except Exception as e:
            self.fail(e)
