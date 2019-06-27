from selia.views.utils import SeliaListView
from irekua_utils.filters.data_collections import data_collections

from database.models import Collection


class UserCollectionsView(SeliaListView):
    template_name = 'selia/collections/user.html'
    filter_class = data_collections.Filter
    search_fields = data_collections.search_fields
    ordering_fields = data_collections.ordering_fields

    def get_initial_queryset(self):
        return self.request.user.collection_users.all()
