from django import forms

from database.models import Item
from selia.views.components.grid import GridView
from rest.filters.items import Filter


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_file',
            'metadata',
            'captured_on',
        ]


class SamplingEventDeviceItems(GridView):
    template_name = 'selia/sampling_event_devices/items.html'
    table_view_name = 'rest-api:samplingeventdevice-items'
    filter_class = Filter
    update_form = UpdateForm

    include_map = False
    with_table_link = True

    update_form_url = '/selia/widgets/update_form/Item/'

    def get_table_url_kwargs(self):
        sampling_event_device_id = self.kwargs['sampling_event_device_id']
        return {"pk": sampling_event_device_id}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        context['sampling_event_device_id'] = kwargs['sampling_event_device_id']
        return context
