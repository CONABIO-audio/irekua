from django import forms

from database.models import PhysicalDevice
from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


class PhysicalDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            'identifier',
            'serial_number',
        ]


class DetailPhysicalDeviceView(SeliaDetailView):
    model = PhysicalDevice
    form_class = PhysicalDeviceUpdateForm

    template_name = 'selia/detail/physical_device.html'

    help_template = 'selia/components/help/physical_device.html'
    detail_template = 'selia/components/details/physical_device.html'
    summary_template = 'selia/components/summaries/physical_device.html'
    update_form_template = 'selia/components/update/physical_device.html'

    delete_redirect_url = 'selia:user_devices'

    def has_view_permission(self):
        return self.object.created_by == self.request.user
