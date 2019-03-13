from uuid import uuid4

from rest_framework.test import APITestCase
from django.urls import reverse

from database.models import TermType
from database.utils import simple_JSON_schema
from rest.serializers import EventTypeSerializer
from rest.views import EventTypeViewSet

from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class EventTypeTestCase(BaseTestCase, APITestCase):
    serializer = EventTypeSerializer
    VIEW_TERM_TYPES = 'View Term Types'
    ADD_TERM_TYPE = 'Add Term Type'
    REMOVE_TERM_TYPE = 'Remove Term Type'
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.ADMIN],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN],
        Actions.DESTROY: [
            Users.ADMIN],
        VIEW_TERM_TYPES: Users.ALL_AUTHENTICATED_USERS,
        ADD_TERM_TYPE: [
            Users.ADMIN
        ],
        REMOVE_TERM_TYPE: [
            Users.ADMIN
        ]
    })

    def __init__(self, *args, **kwargs):
        super(EventTypeTestCase, self).__init__(*args, **kwargs)
        self.VIEW_NAME_MAPPING.update({
            self.VIEW_TERM_TYPES: EventTypeViewSet.label_types.url_name,
            self.ADD_TERM_TYPE: EventTypeViewSet.add_label_type.url_name,
            self.REMOVE_TERM_TYPE: EventTypeViewSet.remove_label_type.url_name
        })

    @staticmethod
    def generate_random_json_data():
        data = {
            'name': str(uuid4()),
            'description': 'Random event type',
        }
        return data

    def setUp(self):
        super(EventTypeTestCase, self).setUp()

        self.event_type = self.create_random_object()
        self.term_type = TermType.objects.create(
            name=str(uuid4()),
            description='random term type',
            is_categorical=True,
            metadata_schema=simple_JSON_schema(),
            synonym_metadata_schema=simple_JSON_schema())

    def test_view_term_type(self):
        permissions = self.permissions[self.VIEW_TERM_TYPES]
        url_name = self.get_url_name(self.VIEW_TERM_TYPES)
        url = reverse(url_name, args=[self.event_type.pk])

        for user_type in Users.ALL_USERS:
            self.change_user(user_type)
            response = self.client.get(url)

            self.check_response(
                Actions.LIST,
                response,
                permissions[user_type],
                user_type)

    def test_add_term_type(self):
        permissions = self.permissions[self.ADD_TERM_TYPE]
        url_name = self.get_url_name(self.ADD_TERM_TYPE)
        url = reverse(url_name, args=[self.event_type.pk])

        payload = {
            'name': self.term_type.name
        }

        for user_type in Users.ALL_USERS:
            self.change_user(user_type)

            try:
                self.event_type.label_term_types.remove(self.term_type)
            except:
                pass

            response = self.client.post(url, payload, format='json')

            self.check_response(
                Actions.CREATE,
                response,
                permissions[user_type],
                user_type)

    def test_remove_term_type(self):
        permissions = self.permissions[self.REMOVE_TERM_TYPE]
        url_name = self.get_url_name(self.REMOVE_TERM_TYPE)
        url = reverse(url_name, args=[self.event_type.pk])

        payload = {
            'name': self.term_type.name
        }

        for user_type in Users.ALL_USERS:
            self.change_user(user_type)

            try:
                self.event_type.label_term_types.add(self.term_type)
            except:
                pass

            response = self.client.post(url, payload, format='json')

            self.check_response(
                Actions.DESTROY,
                response,
                permissions[user_type],
                user_type)
