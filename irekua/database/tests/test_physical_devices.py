from django.test import TestCase

from database.models import PhysicalDevice

from .test_devices import create_simple_device
from .test_users import create_simple_user


def create_simple_physical_device():
    device = create_simple_device()
    user = create_simple_user()

    metadata = {
        'sample_required_parameter': 20
    }

    physical_device, _ = PhysicalDevice.objects.get_or_create(
        serial_number='123456789',
        device=device,
        defaults=dict(
            owner=user,
            metadata=metadata,
            bundle=False)
    )

    return physical_device


class PhysicalDeviceTestCase(TestCase):
    def setUp(self):
        self.physical_device = create_simple_physical_device()

    def test_simple_physical_device_creation(self):
        try:
            create_simple_physical_device()
        except Exception as e:
            self.fail(e)
