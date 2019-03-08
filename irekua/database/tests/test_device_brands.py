from django.test import TestCase

from database.models import DeviceBrand

from . import sample


def create_simple_device_brand():
    device_brand, _ = DeviceBrand.objects.get_or_create(
        name=sample.DEVICE_BRAND)
    return device_brand


class DeviceBrandTestCase(TestCase):
    def test_simple_device_brand_creation(self):
        try:
            create_simple_device_brand()
        except Exception as e:
            self.fail(e)
