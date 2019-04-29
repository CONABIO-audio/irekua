from django import forms

from database.models import CollectionDevice
from selia.views.components.grid import GridView
from rest.filters.collection_devices import Filter


class AddDeviceForm(forms.ModelForm):
    class Meta:
        model = CollectionDevice
        fields = [
            'physical_device',
            'internal_id',
            'metadata',
        ]

class UpdateForm(forms.ModelForm):
    class Meta:
        model = CollectionDevice
        fields = [
            'internal_id',
            'metadata',
        ]


class CollectionDevices(GridView):
    template_name = 'selia/collections/detail/devices.html'
    table_view_name = 'rest-api:collection-devices'
    filter_class = Filter
    update_form = UpdateForm

    include_map = False

    def get_table_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['create_form'] = AddDeviceForm()
        return context
