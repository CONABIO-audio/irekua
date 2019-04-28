from selia.views.components.grid import GridView
from rest.filters.sampling_events import Filter


class UserSamplingEvents(GridView):
    template_name = 'selia/user/grid.html'
    table_view_name = 'rest-api:user-sampling-events'
    map_view_name = 'rest-api:user-sampling-event-locations'

    filter_class = Filter

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}

    def get_map_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
