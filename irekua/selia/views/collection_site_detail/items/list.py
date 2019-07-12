from database.models import CollectionSite
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from database.models import Item

from irekua_utils.filters.items import items
from selia.views.utils import SeliaListView



class CollectionSiteItemsListView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/collection_site_detail/items/list.html'
    list_item_template = 'selia/components/list_items/item.html'
    help_template = 'selia/components/help/collection_site_items.html'
    filter_form_template = 'selia/components/filters/item.html'

    empty_message = _('No items are registered in this collection site')

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=CollectionSite.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection_site=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_site'] = self.object
        return context