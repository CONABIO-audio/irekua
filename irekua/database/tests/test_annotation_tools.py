from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import (
    AnnotationTool,
    Schema
)

SAMPLE_ANNOTATION_TOOL_CONFIGURATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Configuration Schema",
    "required": [
        "parameter1",
        "nested_parameters"
    ],
    "properties": {
        "parameter1": {
            "type": "integer",
            "examples": [
                2
            ]
            },
        "parameter2": {
            "type": "string",
            "examples": [
                "ab"
                ]
            },
        "nested_parameters": {
            "type": "object",
            "required": [
                "subparameter1",
                ],
            "properties": {
                "subparameter1": {
                    "type": "number",
                    "examples": [
                        1.2
                    ]
                    },
                "subparameter2": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "examples": [
                            "a",
                            "b"
                        ],
                    }
                }
            }
        }
    }
}


def create_simple_annotation_tool():
    schema, _ = Schema.objects.get_or_create(
        field='device_configuration',
        name='Sample Device Configuration',
        description='Sample device configuration schema',
        schema=SAMPLE_ANNOTATION_TOOL_CONFIGURATION_SCHEMA)

    annotation_tool, _ = AnnotationTool.objects.get_or_create(
        name="Annotation Tool",
        version="1.0",
        description="Sample Annotation tool",
        configuration_schema=schema)

    return annotation_tool


class AnnotationToolTestCase(TestCase):


    def setUp(self):
        self.annotation_tool = create_simple_annotation_tool()


    def test_simple_annotation_tool_creation(self):
        try:
            create_simple_annotation_tool()
        except:
            self.fail('Creation of Annotation Tool failed')

    def test_validate_configuration(self):
        valid_configuration = {
            "parameter1": 10,
            "nested_parameters": {
                "subparameter1": 6.5
            }
        }

        try:
            self.annotation_tool.validate_configuration(valid_configuration)
        except ValidationError:
            self.fail('Valid JSON was rejected')

        invalid_configuration = {
            "parameter1": "ab"
        }

        with self.assertRaises(ValidationError):
            self.annotation_tool.validate_configuration(invalid_configuration)
