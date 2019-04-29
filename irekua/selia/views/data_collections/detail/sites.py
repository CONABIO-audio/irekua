from selia.views.components.grid import GridView
from rest.filters.sites import Filter


class CollectionSites(GridView):
    template_name = 'selia/collections/detail/sites.html'
    table_view_name = 'rest-api:collection-sites'
    map_view_name = 'rest-api:collection-site-locations'
    filter_class = Filter


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
