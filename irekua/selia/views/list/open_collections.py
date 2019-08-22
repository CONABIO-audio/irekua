from database.models import Collection
from selia.views.list import SeliaListView
from irekua_utils.filters.data_collections import data_collections


class OpenCollectionsView(SeliaListView):
    template_name = 'selia/collections/open.html'
    list_item_template = 'selia/components/list_items/collection.html'
    help_template = 'selia/components/help/open_collections.html'
    filter_form_template = 'selia/components/filters/collection.html'

    filter_class = data_collections.Filter
    search_fields = data_collections.search_fields
    ordering_fields = data_collections.ordering_fields

    def get_initial_queryset(self):
        return Collection.objects.filter(is_open=True)
