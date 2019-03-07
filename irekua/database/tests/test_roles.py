from django.test import TestCase

from database.models import Role


def create_simple_role():
    role, _ = Role.objects.get_or_create(
        name='Sample Role',
        defaults=dict(description='sample role')
    )
    return role

class RoleTypeTestCase(TestCase):
    def setUp(self):
        self.role = create_simple_role()

    def test_simple_role_creation(self):
        try:
            create_simple_role()
        except Exception as e:
            self.fail(e)
