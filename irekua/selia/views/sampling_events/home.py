from django import forms

from database.models import SamplingEvent
from selia.views.components.grid import GridView


class UpdateForm(forms.ModelForm):
    class Meta:
        model = SamplingEvent
        fields = [
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
        ]


class SamplingEventHome(GridView):
    template_name = 'selia/sampling_events/home.html'
    map_view_name = 'rest-api:samplingevent-location'
    detail_view_name = 'rest-api:samplingevent-detail'
    update_form = UpdateForm

    include_table = False
    detail = True

    update_form_url = '/selia/widgets/update_form/SamplingEvent/'

    def get_object_pk(self):
        return self.kwargs['sampling_event_id']

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['sampling_event_id']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        return context
