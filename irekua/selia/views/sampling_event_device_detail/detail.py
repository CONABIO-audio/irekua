from django.views.generic.detail import SingleObjectMixin
from django import forms

from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField
from database.models import SamplingEventDevice

class SamplingEventDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEventDevice
        fields = [
            'metadata',
            'commentaries',
            'configuration',
        ]

class SamplingEventDeviceDetailView(SeliaDetailView, SingleObjectMixin):
    model = SamplingEventDevice
    form_class = SamplingEventDeviceUpdateForm
    template_name = 'selia/sampling_event_device_detail/detail.html'
    help_template = 'selia/components/help/sampling_event_device_detail.html'
    summary_template = 'selia/components/summaries/sampling_event_device.html'
    detail_template = 'selia/components/details/sampling_event_device.html'
    update_form_template = 'selia/components/update/sampling_event_device.html'

    def get_context_data(self, *args, **kwargs):
        sampling_event_device = self.object

        context = super().get_context_data(*args, **kwargs)
        context['sampling_event_device'] = sampling_event_device
        return context

