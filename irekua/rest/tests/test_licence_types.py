from uuid import uuid4

from rest_framework.test import APITestCase

from database.utils import simple_JSON_schema
from rest.serializers import LicenceTypeSerializer
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class LicenceTypeTestCase(BaseTestCase, APITestCase):
    serializer = LicenceTypeSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [Users.ADMIN],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN],
        Actions.DESTROY: [
            Users.ADMIN],
    })

    @staticmethod
    def generate_random_json_data():
        data = {
            'name': str(uuid4()),
            'description': 'Random licence type',
            'metadata_schema': simple_JSON_schema(),
            'years_valid_for': 3,
            'document_template': None,
            'can_view': False,
            'can_download': False,
            'can_view_annotations': False,
            'can_annotate': False,
            'can_vote_annotations': False,
        }
        return data
