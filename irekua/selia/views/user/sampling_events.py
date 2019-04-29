from selia.views.components.grid import GridView
from rest.filters.sampling_events import Filter
from django import forms


from database.models import SamplingEvent


class SamplingEventUpdateForm(forms.ModelForm):
    class Meta:
        model = SamplingEvent
        fields = ['commentaries','metadata','started_on','ended_on']

class UserSamplingEvents(GridView):
    template_name = 'selia/user/grid.html'
    table_view_name = 'rest-api:user-sampling-events'
    map_view_name = 'rest-api:user-sampling-event-locations'
    update_form = SamplingEventUpdateForm

    filter_class = Filter

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}

    def get_map_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
