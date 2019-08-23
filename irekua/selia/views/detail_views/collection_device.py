from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import CollectionDevice
from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionDeviceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionDevice
        fields = [
            'internal_id',
            'metadata',
        ]


class DetailCollectionDeviceView(SeliaDetailView, SingleObjectMixin):
    model = CollectionDevice
    form_class = CollectionDeviceUpdateForm
    delete_redirect_url = 'selia:collection_sampling_events'

    template_name = 'selia/detail/collection_device.html'

    help_template = 'selia/components/help/collection_device_detail.html'
    detail_template = 'selia/components/details/collection_device.html'
    summary_template = 'selia/components/summaries/collection_device.html'
    update_form_template = 'selia/components/update/collection_device.html'

    def get_delete_redirect_url_args(self):
        return [self.object.collection.pk]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_device'] = self.object
        context['collection'] = self.object.collection
        return context
