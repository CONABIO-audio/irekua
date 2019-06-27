from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator

from database.models import Collection, Licence
from selia.views.utils import SeliaListView
from irekua_utils.filters.data_collections import collection_licences

class CollectionLicencesListView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/collection_detail/licence_list.html'
    filter_class = collection_licences.Filter
    search_fields = collection_licences.search_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Licence.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
