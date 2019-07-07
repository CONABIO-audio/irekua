from selia.views.utils import SeliaListView
from irekua_utils.filters.data_collections import data_collections


class UserCollectionsView(SeliaListView):
    template_name = 'selia/collections/user.html'
    list_item_template = 'selia/components/list_items/collection.html'
    help_template = 'selia/components/help/user_collections.html'
    filter_form_template = 'selia/components/filters/collection.html'

    filter_class = data_collections.Filter
    search_fields = data_collections.search_fields
    ordering_fields = data_collections.ordering_fields

    def get_initial_queryset(self):
        return self.request.user.collection_users.all()

    def has_view_permission(self):
        return self.request.user.is_authenticated
