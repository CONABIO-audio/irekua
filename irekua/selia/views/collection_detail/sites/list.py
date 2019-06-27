from django.views.generic.detail import SingleObjectMixin

from database.models import Collection
from database.models import CollectionSite

from selia.views.utils import SeliaListView

from irekua_utils.filters.data_collections import collection_sites


class CollectionSitesListView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/collection_detail/sites/list.html'
    filter_class = collection_sites.Filter
    search_fields = collection_sites.search_fields
    ordering_fields = collection_sites.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return CollectionSite.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
