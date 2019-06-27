from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from database.models import Collection
from database.models import Item

from irekua_utils.filters.items import items
from selia.views.utils import SeliaListView



class CollectionItemsListView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/collection_detail/item_list.html'
    empty_message = _('No items are registered in this collection')
    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
