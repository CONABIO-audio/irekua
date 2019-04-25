from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import serializers

from database.models import PhysicalDevice
from selia.utils import ModelSerializer


class PhysicalDeviceTable(ModelSerializer):
    device_type = serializers.CharField(
        source='device.device_type')
    brand = serializers.CharField(
        source='device.brand')
    model = serializers.CharField(
        source='device.model')

    class Meta:
        model = PhysicalDevice
        fields = ['id', 'device_type', 'brand', 'model', 'serial_number']


@login_required(login_url='registration:login')
def user_devices(request):
    user = request.user
    devices = user.physicaldevice_set.all()

    table = PhysicalDeviceTable(devices, many=True)
    context = {'table': table}
    return render(request, 'selia/user/devices.html', context)
