from django.test import TestCase

from database.models import Role

from . import sample


def create_simple_role():
    role, _ = Role.objects.get_or_create(
        name=sample.ROLE,
        defaults=dict(description='sample role')
    )
    return role


class RoleTypeTestCase(TestCase):
    def test_simple_role_creation(self):
        try:
            create_simple_role()
        except Exception as e:
            self.fail(e)
