from django.test import TestCase

from database.models import EventType

from .test_term_types import create_simple_term_type


def create_simple_event_type():
    event_type, _ = EventType.objects.get_or_create(
        name='Sample Event Type',
        defaults=dict(description='Sample event type')
    )

    term_type = create_simple_term_type()
    event_type.label_term_types.add(term_type)

    return event_type


class EventTypeTestCase(TestCase):
    def setUp(self):
        self.event_type = create_simple_event_type()

    def test_simple_event_type_creation(self):
        try:
            create_simple_event_type()
        except Exception as e:
            self.fail(e)
