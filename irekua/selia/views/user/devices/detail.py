from django import forms

from database.models import PhysicalDevice
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField


class PhysicalDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            'serial_number',
            'bundle',
        ]


class UserPhysicalDeviceDetailView(SeliaDetailView):
    model = PhysicalDevice
    form_class = PhysicalDeviceUpdateForm
    template_name = 'selia/user/devices/detail.html'
    help_template = 'selia/components/help/physical_device.html'
    detail_template = 'selia/components/details/physical_device.html'
    summary_template = 'selia/components/summaries/physical_device.html'
    update_form_template = 'selia/components/update/physical_device.html'
