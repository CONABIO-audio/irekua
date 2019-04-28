from selia.views.components.grid import GridView
from rest.filters.physical_devices import Filter


class TestView(GridView):
    table_view_name = 'rest-api:device-physical-devices'
    filter_class = Filter
    with_table_links = True
    child_view_name = 'selia:collections'
