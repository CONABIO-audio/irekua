from django.test import TestCase

from database.models import Site

from .test_site_types import create_simple_site_type
from .test_users import create_simple_user
from . import sample


def create_simple_site():
    site_type = create_simple_site_type()
    user = create_simple_user()
    metadata = sample.VALID_INSTANCE

    site, _ = Site.objects.get_or_create(
        name=sample.SITE,
        defaults=dict(
            site_type=site_type,
            latitude=0,
            longitude=0,
            altitude=0,
            metadata=metadata,
            creator=user)
    )

    return site


class SiteTestCase(TestCase):
    def test_simple_site_type_creation(self):
        try:
            create_simple_site()
        except Exception as e:
            self.fail(e)
