from django.db.models import Q

from database.models import SamplingEvent
from database.models import SamplingEventType
from database.models import Collection
from database.models import CollectionDevice

from irekua_utils.filters.sampling_events import sampling_events as sampling_event_utils
from irekua_utils.permissions.sampling_events import (
    devices as device_permissions)

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectSamplingEventDeviceSamplingEventView(SeliaSelectView):
    template_name = 'selia/create/sampling_event_devices/select_sampling_event.html'
    prefix = 'sampling_event'
    create_url = 'selia:create_sampling_event_device'

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                name=self.request.GET['collection'])

    def has_view_permission(self):
        user = self.request.user
        return device_permissions.create(user, collection=self.collection)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.collection
        return context

    def get_queryset(self):
        collection_pk = self.request.GET['collection']

        queryset = SamplingEvent.objects.filter(collection__name=collection_pk)

        if 'collection_device' in self.request.GET:
            collection_device_pk = self.request.GET['collection_device']
            collection_device = CollectionDevice.objects.get(pk=collection_device_pk)

            query = (
                Q(restrict_device_types=False) |
                Q(device_types=collection_device.physical_device.device.device_type)
            )
            valid_types = SamplingEventType.objects.filter(query)

            print(valid_types.all())

            queryset = queryset.filter(sampling_event_type__in=valid_types)

        return queryset

    def get_list_class(self):

        class SamplingEventList(SeliaList):
            filter_class = sampling_event_utils.Filter
            search_fields = sampling_event_utils.search_fields
            ordering_fields = sampling_event_utils.ordering_fields

            queryset = self.get_queryset()

            list_item_template = 'selia/components/select_list_items/sampling_events.html'
            filter_form_template = 'selia/components/filters/sampling_event.html'

        return SamplingEventList
