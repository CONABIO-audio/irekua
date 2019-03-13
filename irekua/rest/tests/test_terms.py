from uuid import uuid4

from rest_framework.test import APITestCase
from database.utils import simple_JSON_schema
from database.models import TermType
from rest.serializers import TermSerializer
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)


class TermTestCase(BaseTestCase, APITestCase):
    serializer = TermSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.ADMIN,
            Users.DEVELOPER],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN,
            Users.DEVELOPER],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN,
            Users.DEVELOPER],
        Actions.DESTROY: [
            Users.ADMIN,
            Users.DEVELOPER],
    })

    def setUp(self):
        super().setUp()
        TermType.objects.create(
            name='sample term type',
            description='random term type',
            is_categorical=True)

    @staticmethod
    def generate_random_json_data():
        data = {
            'term_type': 'sample term type',
            'value': str(uuid4()),
            'metadata': {},
        }
        return data
