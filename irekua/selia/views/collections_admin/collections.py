from database.models import Collection
from selia.views.utils import SeliaListView
from irekua_utils.filters.admin import managed_collections


class ManagedCollectionsView(SeliaListView):
    template_name = 'selia/collections_admin/managed_collections.html'
    list_item_template = 'selia/components/list_items/managed_collection.html'
    help_template = 'selia/components/help/managed_collections.html'
    filter_form_template = 'selia/components/filters/managed_collection.html'

    filter_class = managed_collections.Filter
    search_fields = managed_collections.search_fields
    ordering_fields = managed_collections.ordering_fields

    def get_initial_queryset(self):
        user = self.request.user
        collection_types = user.collectiontype_set.all()
        return Collection.objects.filter(collection_type__in=collection_types)
