from selia.views.components.grid import GridView
from rest.filters.items import Filter


class UserItems(GridView):
    template_name = 'selia/user/items.html'
    table_view_name = 'rest-api:user-items'
    map_view_name = 'rest-api:user-item-locations'
    filter_class = Filter

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}

    def get_map_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
