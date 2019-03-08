from django.test import TestCase
from django.core.exceptions import ValidationError

from database.models import (
    AnnotationVote,
    TermType,
    Term,
)

from .test_annotations import create_simple_annotation
from .test_users import create_simple_user
from .test_terms import create_simple_term
from .test_schemas import create_simple_schema
from . import sample


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
        except Exception as e:
            self.fail(e)

    def test_label_validation(self):
        annotation = create_simple_annotation()
        user = create_simple_user()

        label = {
            'Sample Invalid Term Type': 'Sample Invalid Term Value'
        }

        with self.assertRaises(ValidationError):
            AnnotationVote.objects.create(
                annotation=annotation,
                label=label,
                created_by=user)

        schema = create_simple_schema()
        term_type, _ = TermType.objects.get_or_create(
            name='Sample Invalid Term Type',
            defaults={
                'description': 'Sample invalid term type',
                'is_categorical': True,
                'metadata_schema': schema,
                'synonym_metadata_schema': schema
            })

        term, _ = Term.objects.get_or_create(
            term_type=term_type,
            value='Sample Invalid Term Value',
            metadata=sample.VALID_INSTANCE)

        annotation.event_type.label_term_types.add(term_type)
        annotation.save()

        try:
            AnnotationVote.objects.create(
                annotation=annotation,
                label=label,
                created_by=user)
        except ValidationError as e:
            self.fail(e)
        finally:
            term.delete()
            term_type.delete()
