from django.test import TestCase
from django.core.exceptions import ValidationError

from database.models import (
    AnnotationVote,
    TermType,
    Term,
    Schema,
    EventType,
)

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
        except Exception as e:
            self.fail(e)

    def test_label_validation(self):
        annotation = create_simple_annotation()
        user = create_simple_user()

        try:
            term = Term.objects.get(
                term_type='Sample Invalid Term Type',
                value='Sample Invalid Term Value')
            term.delete()
        except Term.DoesNotExist:
            pass

        label = {
            'Sample Invalid Term Type': 'Sample Invalid Term Value'
        }

        with self.assertRaises(ValidationError):
            AnnotationVote.objects.create(
                annotation=annotation,
                label=label,
                created_by=user)

        free_schema = Schema.objects.get(name=Schema.FREE_SCHEMA)

        term_type, _ = TermType.objects.get_or_create(
            name='Sample Invalid Term Type',
            defaults={
                'description': 'Sample invalid term type',
                'is_categorical': True,
                'metadata_schema': free_schema,
                'synonym_metadata_schema': free_schema
            })
        event_type = EventType.objects.get(name='Sample Event Type')

        term, _ = Term.objects.get_or_create(
            term_type=term_type,
            value='Sample Invalid Term Value')

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
