from django import forms

from database.models import Device
from database.models import PhysicalDevice

from selia.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView


class PhysicalDeviceCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = PhysicalDevice
        fields = [
            'device',
            'metadata',
            'serial_number',
            'identifier',
            'bundle'
        ]


class CreatePhysicalDeviceView(SeliaCreateView):
    model = PhysicalDevice
    form_class = PhysicalDeviceCreateForm

    template_name = 'selia/create/physical_devices/create_form.html'
    success_url = 'selia:user_physical_devices'

    def get_success_url_args(self):
        return []

    def get_initial(self):
        self.device = Device.objects.get(
            pk=self.request.GET['device'])

        return {
            'device': self.device,
            'bundle': True,
        }

    def get_additional_query_on_sucess(self):
        return {
            'physical_device': self.object.pk
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['device'] = self.device
        context['form'].fields['metadata'].update_schema(
            self.device.metadata_schema)

        return context
