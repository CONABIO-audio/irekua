from selia.views.components.grid import GridView
from rest.filters.data_collections import Filter


class OpenCollections(GridView):
    template_name = 'selia/collections/open_collections.html'
    table_view_name = 'rest-api:collection-list'
    filter_class = Filter

    include_detail = False
    include_map = False
    include_summary = False

    with_table_links = True
    child_view_name = 'selia:collection_home'
