from django import forms

from database.models import SamplingEventDevice
from selia.views.components.grid import GridView


class UpdateForm(forms.ModelForm):
    class Meta:
        model = SamplingEventDevice
        fields = [
            "commentaries",
            "metadata",
            "configuration",
        ]


class SamplingEventDeviceHome(GridView):
    template_name = 'selia/sampling_event_devices/home.html'
    map_view_name = 'rest-api:samplingeventdevice-location'
    detail_view_name = 'rest-api:samplingeventdevice-detail'
    update_form = UpdateForm

    include_map = True
    include_table = False
    detail = True

    def get_object_pk(self):
        pk = self.kwargs['sampling_event_device_id']
        return pk

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        context['sampling_event_device_id'] = kwargs['sampling_event_device_id']
        return context
