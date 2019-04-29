from django import forms

from database.models import Item
from selia.views.components.grid import GridView
from rest.filters.items import Filter


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_file',
            'metadata',
            'captured_on',
        ]


class SamplingEventItems(GridView):
    template_name = 'selia/sampling_events/items.html'
    table_view_name = 'rest-api:samplingevent-items'
    filter_class = Filter
    update_form = UpdateForm

    include_map = False

    def get_table_url_kwargs(self):
        sampling_event_id = self.kwargs['sampling_event_id']
        return {"pk": sampling_event_id}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['sampling_event_id'] = kwargs['sampling_event_id']
        return context
