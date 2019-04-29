from selia.views.components.grid import GridView


class SamplingEventDeviceHome(GridView):
    template_name = 'selia/sampling_event_devices/base.html'
    map_view_name = 'rest-api:samplingeventdevice-location'

    include_map = True
    include_table = False

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        context['sampling_event_device_id'] = kwargs['sampling_event_device_id']
        return context
