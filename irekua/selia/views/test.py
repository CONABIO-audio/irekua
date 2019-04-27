from selia.views.components.grid import GridView
from rest.filters.physical_devices import Filter


class TestView(GridView):
    filter_class = Filter
