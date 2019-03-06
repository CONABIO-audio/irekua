from django.test import TestCase

# Create your tests here.
from database.models import Annotation



def create_simple_annotation():
    return None


class AnnotationTestCase(TestCase):
    def setUp(self):
        self.annotation = create_simple_annotation()

    def test_simple_annotation_creation(self):
        try:
            create_simple_annotation()
        except:
            self.fail('Annotation creation failed')
