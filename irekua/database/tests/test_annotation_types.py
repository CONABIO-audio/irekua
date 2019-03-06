from django.test import TestCase
from django.core.exceptions import ValidationError
# Create your tests here.

from database.models import (
    AnnotationType,
    Schema
)

SAMPLE_ANNOTATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "BBox Annotation",
    "required": [
        "x",
        "y",
        "height",
        "width"
    ],
    "properties": {
        "x": {
            "type": "integer"
        },
        "y": {
            "type": "integer"
        },
        "height": {
            "type": "integer",
        },
        "width": {
            "type": "integer",
        }
    }
}

def create_simple_annotation_type():
    schema, _ = Schema.objects.get_or_create(
        field='annotation',
        name='Sample Annotation Schema',
        description="Sample annotation schema",
        schema=SAMPLE_ANNOTATION_SCHEMA)

    annotation_type, _ = AnnotationType.objects.get_or_create(
        name='Sample Annotation Type',
        description='sample annotation type',
        schema=schema)

    return annotation_type


class AnnotationTypeTestCase(TestCase):
    def setUp(self):
        self.annotation_type = create_simple_annotation_type()

    def test_simple_annotation_type_creation(self):
        try:
            create_simple_annotation_type()
        except:
            self.fail('Creation of annotation type failed')

    def test_validate_annotation(self):
        valid_annotation = {
            "x": 20,
            "y": 50,
            "height": 100,
            "width": 50
        }
        try:
            self.annotation_type.validate_annotation(valid_annotation)
        except ValidationError:
            self.fail('Valid annotation was deemed invalid')

        invalid_annotation = {
            "y": 50,
            "height": 100,
            "width": 50
        }
        with self.assertRaises(ValidationError):
            self.annotation_type.validate_annotation(invalid_annotation)
