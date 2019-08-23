from django.views.generic import TemplateView

from database.models import Collection
from database.models import CollectionSite
from database.models import SamplingEventType
from irekua_utils.filters.data_collections import collection_sites as site_utils
from selia.views.utils import SeliaList


class SelectSamplingEventSiteView(TemplateView):
    template_name = 'selia/create/sampling_events/select_site.html'

    def get_context_data(self):
        context = super().get_context_data()
        collection = Collection.objects.get(pk=self.request.GET['collection'])
        context['collection'] = collection
        context['collection_site_list'] = self.get_collection_site_list_list(collection)
        return context

    def get_collection_site_list_list(self, collection):
        collection_sites = CollectionSite.objects.filter(collection=collection)

        sampling_event_type = SamplingEventType.objects.get(
            pk=self.request.GET['sampling_event_type'])

        if sampling_event_type.restrict_site_types:
            collection_sites = collection_sites.filter(
                site_type__in=sampling_event_type.site_types.all())

        class CollectionSiteList(SeliaList):
            prefix = 'collection'

            filter_class = site_utils.Filter
            search_fields = site_utils.search_fields
            ordering_fields = site_utils.ordering_fields

            queryset = collection_sites

            list_item_template = 'selia/components/select_list_items/collection_sites.html'
            filter_form_template = 'selia/components/filters/collection_site.html'

        collection_site_list = CollectionSiteList()
        return collection_site_list.get_context_data(self.request)
