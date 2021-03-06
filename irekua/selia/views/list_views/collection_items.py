from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from database.models import Collection
from database.models import Item

from irekua_utils.filters.items import items
from irekua_utils.permissions.items import (
    items as item_permissions)
from irekua_utils.permissions.data_collections import (
    users as user_permissions)
from irekua_utils.permissions import (
    licences as licence_permissions)

from selia.views.list_views.base import SeliaListView


class ListCollectionItemsView(SeliaListView, SingleObjectMixin):
    template_name = 'selia/list/collection_items.html'

    list_item_template = 'selia/components/list_items/item.html'
    help_template = 'selia/components/help/collection_items.html'
    filter_form_template = 'selia/components/filters/item.html'

    empty_message = _('No items are registered in this collection')

    filter_class = items.Filter
    search_fields = items.search_fields
    ordering_fields = items.ordering_fields

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.list(user, collection=self.object)

    def has_create_permission(self):
        user = self.request.user
        return item_permissions.create(user, collection=self.object)

    def get_permissions(self):
        permissions = super().get_permissions()
        user = self.request.user
        permissions['list_collection_users'] = user_permissions.list(
                user, collection=self.object)
        permissions['list_collection_licences'] = licence_permissions.list(
                user, collection=self.object)
        return permissions

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
