from django.test import TestCase
from django.core.exceptions import ValidationError

from database.models import (
    AnnotationType,
    Schema
)

from . import sample


def create_simple_annotation_type():
    schema, _ = Schema.objects.get_or_create(
        name=sample.ANNOTATION_SCHEMA.name,
        defaults=dict(
            field='annotation',
            description="Sample annotation schema",
            schema=sample.ANNOTATION_SCHEMA.schema)
    )

    annotation_type, _ = AnnotationType.objects.get_or_create(
        name=sample.ANNOTATION_TYPE,
        defaults=dict(
            description='sample annotation type',
            schema=schema)
    )

    return annotation_type


class AnnotationTypeTestCase(TestCase):
    def setUp(self):
        self.annotation_type = create_simple_annotation_type()

    def test_simple_annotation_type_creation(self):
        try:
            create_simple_annotation_type()
        except Exception as e:
            self.fail(e)

    def test_validate_annotation(self):
        valid_annotation = sample.VALID_ANNOTATION
        try:
            self.annotation_type.validate_annotation(valid_annotation)
        except ValidationError:
            self.fail()

        invalid_annotation = sample.INVALID_ANNOTATION
        with self.assertRaises(ValidationError):
            self.annotation_type.validate_annotation(invalid_annotation)
