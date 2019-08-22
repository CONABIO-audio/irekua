from django.utils.translation import gettext as _

from database.models import Item

from irekua_utils.filters.items import items
from selia.views.utils import SeliaListView



class UserItemsListView(SeliaListView):
    template_name = 'selia/user/items/list.html'
    list_item_template = 'selia/components/list_items/item.html'
    help_template = 'selia/components/help/user_items.html'
    filter_form_template = 'selia/components/filters/item.html'

    empty_message = _('User has no registered items')

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def get_initial_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
