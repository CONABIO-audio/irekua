from database.models import SamplingEventDevice
from database.models import SamplingEvent

from irekua_utils.filters.sampling_events import sampling_event_devices as sampling_event_utils

from selia.views.utils import SeliaList
from selia.views.create import SeliaSelectView


class SelectItemSamplingEventDeviceView(SeliaSelectView):
    template_name = 'selia/create/items/select_sampling_event_device.html'
    prefix = 'sampling_event_device'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['sampling_event'] = SamplingEvent.objects.get(
            pk=self.request.GET['sampling_event'])
        return context

    def get_list_class(self):
        sampling_event = self.request.GET['sampling_event']

        class SamplingEventDeviceList(SeliaList):
            filter_class = sampling_event_utils.Filter
            search_fields = sampling_event_utils.search_fields
            ordering_fields = sampling_event_utils.ordering_fields

            queryset = SamplingEventDevice.objects.filter(sampling_event__pk=sampling_event)

            list_item_template = 'selia/components/select_list_items/sampling_event_devices.html'
            filter_form_template = 'selia/components/filters/sampling_event_device.html'

        return SamplingEventDeviceList
