from selia.views.components.grid import GridView
from rest.filters.items import Filter


class UserItems(GridView):
    template_name = 'selia/user/grid.html'
    table_view_name = 'rest-api:user-items'
    filter_class = Filter

    def get_table_url_kwrags(self):
        user = self.request.user
        return {"pk": user.pk}
