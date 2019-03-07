from django.test import TestCase

# Create your tests here.
from database.models import Annotation

from .test_annotation_tools import create_simple_annotation_tool
from .test_items import create_simple_item
from .test_event_types import create_simple_event_type
from .test_annotation_types import create_simple_annotation_type
from .test_users import create_simple_user
from .test_terms import create_simple_term


def create_simple_annotation():
    annotation_tool = create_simple_annotation_tool()
    item = create_simple_item()
    event_type = create_simple_event_type()
    annotation_type = create_simple_annotation_type()
    user = create_simple_user()
    term = create_simple_term()

    label = {
        term.term_type.name: term.value
    }

    annotation_configuration = {
        'parameter1': 2,
    }

    annotation = {
        'x': 10,
        'y': 20,
        'height': 100,
        'width': 50
    }

    annotation, _ = Annotation.objects.create(
        annotation_tool=annotation_tool,
        item=item,
        event_type=event_type,
        label=label,
        annotation_type=annotation_type,
        annotation=annotation,
        annotation_configuration=annotation_configuration,
        certainty=1,
        quality=Annotation.HIGH_QUALITY,
        commentaries='Sample annotation commentaries',
        created_by=user)

    return annotation


class AnnotationTestCase(TestCase):
    def setUp(self):
        self.annotation = create_simple_annotation()

    def test_simple_annotation_creation(self):
        try:
            create_simple_annotation()
        except:
            self.fail()
