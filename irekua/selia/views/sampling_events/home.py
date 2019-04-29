from selia.views.components.grid import GridView


class SamplingEventHome(GridView):
    template_name = 'selia/sampling_events/base.html'
    map_view_name = 'rest-api:samplingevent-location'

    include_table = False

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['sampling_event_id']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        return context
