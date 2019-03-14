from uuid import uuid4
from random import sample

from rest_framework.test import APITestCase

from database.models import TermType, Term
from database.utils import simple_JSON_schema
from rest.serializers import SynonymSerializer
from .utils import (
    BaseTestCase,
    Users,
    Actions,
    create_permission_mapping_from_lists
)

class SynonymTestCase(BaseTestCase, APITestCase):
    serializer = SynonymSerializer
    permissions = create_permission_mapping_from_lists({
        Actions.LIST: Users.ALL_AUTHENTICATED_USERS,
        Actions.CREATE: [
            Users.ADMIN,
        ],
        Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS,
        Actions.UPDATE: [
            Users.ADMIN,
            ],
        Actions.PARTIAL_UPDATE: [
            Users.ADMIN,
            ],
        Actions.DESTROY: [
            Users.ADMIN,
            ],
        })

    def setUp(self):
        super(SynonymTestCase, self).setUp()
        term_type = TermType.objects.create(
            name=str(uuid4()),
            description='random term type',
            is_categorical=True,
            metadata_schema=simple_JSON_schema(),
            synonym_metadata_schema=simple_JSON_schema())
        self.terms = [
            Term.objects.create(
                term_type=term_type,
                value=str(uuid4()))
            for _ in range(40)
        ]

    def generate_random_json_data(self):
        term1, term2 = sample(self.terms, 2)
        data = {
            'source': term1.pk,
            'target': term2.pk,
            'metadata': {}
        }
        return data