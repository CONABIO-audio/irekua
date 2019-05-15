from selia.views.components.grid import GridView
from rest.filters.data_collections import Filter


class UserCollections(GridView):
    template_name = 'selia/collections/collections.html'
    table_view_name = 'rest-api:user-collections'
    filter_class = Filter

    include_detail = False
    include_map = False
    include_summary = False

    with_table_links = True
    child_view_name = 'selia:collection_home'

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
