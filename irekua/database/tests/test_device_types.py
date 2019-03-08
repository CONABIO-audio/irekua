from django.test import TestCase

from database.models import DeviceType

from . import sample


def create_simple_device_type():
    device_type, _ = DeviceType.objects.get_or_create(
        name=sample.DEVICE_TYPE,
        defaults=dict(description='Sample device type')
    )
    return device_type


class DeviceTypeTestCase(TestCase):
    def testSimpleDeviceTypeCreation(self):
        try:
            create_simple_device_type()
        except Exception as e:
            self.fail(e)
