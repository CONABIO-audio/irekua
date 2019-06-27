from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator

from database.models import Collection, SamplingEvent
from selia.views.utils import SeliaListView
from irekua_utils.filters.data_collections import collection_sampling_events


class CollectionSamplingEventListView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/collection_detail/sampling_event_list.html'
    filter_class = collection_sampling_events.Filter
    search_fields = collection_sampling_events.search_fields
    ordering_fields = collection_sampling_events.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return SamplingEvent.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context