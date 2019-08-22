from django.utils.translation import gettext as _

from database.models import SamplingEvent

from irekua_utils.filters.sampling_events import sampling_events
from selia.views.list import SeliaListView


class UserSamplingEventsListView(SeliaListView):
    template_name = 'selia/user/sampling_events/list.html'
    list_item_template = 'selia/components/list_items/sampling_event.html'
    help_template = 'selia/components/help/user_sampling_events.html'
    filter_form_template = 'selia/components/filters/sampling_event.html'

    empty_message = _('User has no registered sampling events')

    filter_class = sampling_events.Filter
    search_fields = sampling_events.search_fields
    ordering_fields = sampling_events.ordering_fields

    def get_initial_queryset(self):
        return SamplingEvent.objects.filter(created_by=self.request.user)
