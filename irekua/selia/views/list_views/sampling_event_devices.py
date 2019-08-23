from django.views.generic.detail import SingleObjectMixin

from database.models import SamplingEvent, SamplingEventDevice
from selia.views.list_views.base import SeliaListView
from irekua_utils.filters.sampling_events import sampling_event_devices
from django.utils.translation import gettext as _


class ListSamplingEventDevicesView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/sampling_event_devices.html'

    list_item_template = 'selia/components/list_items/sampling_event_device.html'
    help_template = 'selia/components/help/sampling_event_device.html'
    filter_form_template = 'selia/components/filters/sampling_event_device.html'

    empty_message = _('No devices are registered in this sampling event')

    filter_class = sampling_event_devices.Filter
    search_fields = sampling_event_devices.search_fields
    ordering_fields = sampling_event_devices.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SamplingEvent.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return SamplingEventDevice.objects.filter(sampling_event=self.object)

    def get_context_data(self, *args, **kwargs):
        sampling_event = self.object

        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = sampling_event
        return context