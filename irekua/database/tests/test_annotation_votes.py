from django.test import TestCase

# Create your tests here.
from database.models import AnnotationVote


from .test_annotations import create_simple_annotation
from .test_users import create_simple_user
from .test_terms import create_simple_term


def create_simple_annotation_vote():
    annotation = create_simple_annotation()
    user = create_simple_user()
    term = create_simple_term()

    label = {
        term.term_type.name: term.value
    }

    annotation_vote = AnnotationVote.objects.create(
        annotation=annotation,
        label=label,
        created_by=user)

    return annotation_vote


class AnnotationVoteTestCase(TestCase):
    def setUp(self):
        self.annotation = create_simple_annotation_vote()

    def test_simple_annotation_vote_creation(self):
        try:
            create_simple_annotation_vote()
        except:
            self.fail()
