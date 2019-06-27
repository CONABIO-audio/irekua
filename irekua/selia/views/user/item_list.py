from django.utils.translation import gettext as _

from database.models import Item

from irekua_utils.filters.items import items
from selia.views.utils import SeliaListView



class UserItemsListView(SeliaListView):
    template_name = 'selia/user/item_list.html'
    empty_message = _('User has no registered items')
    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def get_initial_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
