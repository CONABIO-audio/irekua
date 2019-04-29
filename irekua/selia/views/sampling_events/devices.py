from selia.views.components.grid import GridView
from rest.filters.sampling_event_devices import Filter


class SamplingEventDevices(GridView):
    template_name = 'selia/sampling_events/devices.html'
    table_view_name = 'rest-api:samplingevent-devices'
    filter_class = Filter

    include_map = False
    with_table_links = True
    child_view_name = 'selia:sampling_event_device_home'

    def get_table_url_kwargs(self):
        sampling_event_id = self.kwargs['sampling_event_id']
        return {"pk": sampling_event_id}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        return context
