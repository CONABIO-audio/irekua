from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from database.models import AnnotationTool

from . import sample


def create_simple_annotation_tool():
    annotation_tool, _ = AnnotationTool.objects.get_or_create(
        name=sample.ANNOTATION_TOOL,
        defaults=dict(
            version="1.0",
            description="Sample Annotation tool",
            configuration_schema=sample.SCHEMA)
    )

    return annotation_tool


class AnnotationToolTestCase(TestCase):
    def setUp(self):
        self.annotation_tool = create_simple_annotation_tool()

    def test_simple_annotation_tool_creation(self):
        try:
            create_simple_annotation_tool()
        except Exception as e:
            self.fail(e)

    def test_validate_configuration(self):
        valid_configuration = sample.VALID_INSTANCE

        try:
            self.annotation_tool.validate_configuration(valid_configuration)
        except ValidationError:
            self.fail('Valid JSON was rejected')

        invalid_configuration = sample.INVALID_INSTANCE

        with self.assertRaises(ValidationError):
            self.annotation_tool.validate_configuration(invalid_configuration)
