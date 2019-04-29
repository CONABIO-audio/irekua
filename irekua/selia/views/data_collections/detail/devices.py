from selia.views.components.grid import GridView
from rest.filters.collection_devices import Filter


class CollectionDevices(GridView):
    template_name = 'selia/collections/detail/base.html'
    table_view_name = 'rest-api:collection-devices'
    filter_class = Filter

    include_map = False

    def get_table_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        return context
