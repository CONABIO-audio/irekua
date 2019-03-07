from django.test import TestCase

# Create your tests here.
from database.models import DeviceType


def create_simple_device_type():
    device_type, _ = DeviceType.objects.get_or_create(
        name='Sample Device Type',
        defaults=dict(description='Sample device type')
    )
    return device_type


class DeviceTypeTestCase(TestCase):
    def setUp(self):
        self.device_type = create_simple_device_type()

    def testSimpleDeviceTypeCreation(self):
        try:
            create_simple_device_type()
        except:
            self.fail('A device type could not be created')
