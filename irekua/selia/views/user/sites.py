from selia.views.components.grid import GridView
from rest.filters.sites import Filter


class UserSites(GridView):
    template_name = 'selia/user/grid.html'
    table_view_name = 'rest-api:user-sites'
    filter_class = Filter

    def get_table_url_kwrags(self):
        user = self.request.user
        return {"pk": user.pk}
