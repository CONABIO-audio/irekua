from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from database.models import Collection, SamplingEvent
from selia.views.list_views.base import SeliaListView
from irekua_utils.filters.sampling_events import sampling_events


class ListCollectionSamplingEventView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/sampling_events.html'

    list_item_template = 'selia/components/list_items/sampling_event.html'
    help_template = 'selia/components/help/collection_sampling_events.html'
    filter_form_template = 'selia/components/filters/sampling_event.html'

    empty_message = _('No sampling events are registered in this sampling event')

    filter_class = sampling_events.Filter
    search_fields = sampling_events.search_fields
    ordering_fields = sampling_events.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return SamplingEvent.objects.filter(collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
