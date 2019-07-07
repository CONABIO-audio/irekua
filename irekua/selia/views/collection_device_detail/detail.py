from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import CollectionDevice
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionDevice
        fields = [
            'internal_id',
            'metadata',
        ]


class CollectionDeviceDetailView(SeliaDetailView, SingleObjectMixin):
    model = CollectionDevice
    form_class = CollectionDeviceUpdateForm

    template_name = 'selia/collection_device_detail/detail.html'
    help_template = 'selia/components/help/collection_device_detail.html'
    detail_template = 'selia/components/details/collection_device.html'
    summary_template = 'selia/components/summaries/collection_device.html'
    update_form_template = 'selia/components/update/collection_device.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_device'] = self.object
        return context
