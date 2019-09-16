from irekua_utils.filters.data_collections import data_collections as collection_utils

from selia.views.utils import SeliaList
from selia.views.create_views import SeliaSelectView


class SelectCollectionSiteCollectionView(SeliaSelectView):
    template_name = 'selia/create/collection_sites/select_collection.html'
    prefix = 'collection'
    create_url = 'selia:create_collection_site'

    def get_list_class(self):
        class CollectionList(SeliaList):
            filter_class = collection_utils.Filter
            search_fields = collection_utils.search_fields
            ordering_fields = collection_utils.ordering_fields

            queryset = self.request.user.collection_users.all()

            list_item_template = 'selia/components/select_list_items/collection.html'
            filter_form_template = 'selia/components/filters/collection.html'

        return CollectionList
