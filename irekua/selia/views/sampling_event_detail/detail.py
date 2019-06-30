from django.views.generic.detail import SingleObjectMixin
from django import forms

from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField
from database.models import SamplingEvent

class SamplingEventUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'metadata',
            'collection_site',
            'commentaries',
            'started_on',
            'ended_on',
            'licence',
        ]


class SamplingEventDetailView(SeliaDetailView, SingleObjectMixin):
    model = SamplingEvent
    form_class = SamplingEventUpdateForm

    template_name = 'selia/sampling_event_detail/detail.html'
    help_template = 'selia/components/help/collection_sampling_events.html'
    summary_template = 'selia/components/summaries/sampling_event.html'
    detail_template = 'selia/components/details/sampling_event.html'
    update_form_template = 'selia/components/update/sampling_event.html'


    def get_context_data(self, *args, **kwargs):
        sampling_event = self.object

        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = sampling_event
        return context
