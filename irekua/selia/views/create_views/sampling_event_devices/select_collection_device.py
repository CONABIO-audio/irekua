from database.models import SamplingEvent
from database.models import CollectionDevice

from irekua_utils.filters.sampling_events import sampling_events as sampling_event_utils

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectSamplingEventDeviceCollectionDeviceView(SeliaSelectView):
    template_name = 'selia/create/sampling_event_devices/select_collection_device.html'
    prefix = 'collection_device'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['sampling_event'] = SamplingEvent.objects.get(
            pk=self.request.GET['sampling_event'])
        return context

    def get_list_class(self):
        collection_pk = self.request.GET['collection']

        class SamplingEventList(SeliaList):
            filter_class = sampling_event_utils.Filter
            search_fields = sampling_event_utils.search_fields
            ordering_fields = sampling_event_utils.ordering_fields

            queryset = CollectionDevice.objects.filter(collection__name=collection_pk)

            list_item_template = 'selia/components/select_list_items/sampling_events.html'
            filter_form_template = 'selia/components/filters/sampling_event.html'

        return SamplingEventList
