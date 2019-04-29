from selia.views.components.grid import GridView
from rest.filters.sampling_events import Filter


class CollectionSamplingEvents(GridView):
    template_name = 'selia/collections/detail/sampling_events.html'
    table_view_name = 'rest-api:collection-sampling-events'
    map_view_name = 'rest-api:collection-sampling-event-locations'
    filter_class = Filter

    with_table_links = True
    child_view_name = 'selia:sampling_event_home'

    def get_table_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        return context
