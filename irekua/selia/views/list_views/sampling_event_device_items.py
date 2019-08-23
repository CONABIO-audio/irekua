from database.models import SamplingEventDevice
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from database.models import Item
from irekua_utils.filters.items import items
from selia.views.list_views.base import SeliaListView


class ListSamplingEventDeviceItemsView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/sampling_event_device_items.html'
    
    list_item_template = 'selia/components/list_items/item.html'
    help_template = 'selia/components/help/sampling_event_device_items.html'
    filter_form_template = 'selia/components/filters/item.html'

    empty_message = _('No items are registered to this sampling event device')

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SamplingEventDevice.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Item.objects.filter(
            sampling_event_device=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event_device'] = self.object
        return context
