from django.test import TestCase

from database.models import DeviceBrand


def create_simple_device_brand():
    device_brand, _ = DeviceBrand.objects.get_or_create(name='Sample Device Brand')
    return device_brand


class DeviceBrandTestCase(TestCase):
    def setUp(self):
        self.device_brand = create_simple_device_brand()

    def test_simple_device_brand_creation(self):
        try:
            create_simple_device_brand()
        except Exception as e:
            self.fail(e)
