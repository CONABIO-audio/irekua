from selia.views.components.grid import GridView
from rest.filters.physical_devices import Filter


class UserDevices(GridView):
    template_name = 'selia/user/grid.html'
    table_view_name = 'rest-api:user-devices'
    filter_class = Filter

    include_map = False

    def get_table_url_kwrags(self):
        user = self.request.user
        return {"pk": user.pk}
