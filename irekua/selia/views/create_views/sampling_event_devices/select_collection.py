from django.views.generic import TemplateView

from database.models import Collection
from irekua_utils.filters.data_collections import data_collections as collection_utils
from selia.views.utils import SeliaList


class SelectSamplingEventDeviceCollectionView(TemplateView):
    template_name = 'selia/create/sampling_event_devices/select_collection.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_list'] = self.get_collection_list()
        return context

    def get_collection_list(self):
        class CollectionList(SeliaList):
            prefix = 'collection'

            filter_class = collection_utils.Filter
            search_fields = collection_utils.search_fields
            ordering_fields = collection_utils.ordering_fields

            queryset = Collection.objects.all()

            list_item_template = 'selia/components/select_list_items/user_collections.html'
            filter_form_template = 'selia/components/filters/collection.html'

        collection_list = CollectionList()
        return collection_list.get_context_data(self.request)
