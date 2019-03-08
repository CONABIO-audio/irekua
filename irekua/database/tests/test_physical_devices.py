from django.test import TestCase

from database.models import PhysicalDevice

from .test_devices import create_simple_device
from .test_users import create_simple_user
from . import sample


def create_simple_physical_device():
    device = create_simple_device()
    user = create_simple_user()
    metadata = sample.VALID_INSTANCE

    physical_device, _ = PhysicalDevice.objects.get_or_create(
        serial_number=sample.DEVICE_SERIAL_NUMBER,
        device=device,
        defaults=dict(
            owner=user,
            metadata=metadata,
            bundle=False)
    )

    return physical_device


class PhysicalDeviceTestCase(TestCase):
    def test_simple_physical_device_creation(self):
        try:
            create_simple_physical_device()
        except Exception as e:
            self.fail(e)
