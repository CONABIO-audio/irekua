from django import forms

from database.models import SamplingEvent
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField


class SamplingEventUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
        ]


class UserSamplingEventDetailView(SeliaDetailView):
    model = SamplingEvent
    form_class = SamplingEventUpdateForm
    template_name = 'selia/user/sampling_events/detail.html'
    help_template = 'selia/components/help/sampling_event.html'
    detail_template = 'selia/components/details/sampling_event.html'
    summary_template = 'selia/components/summaries/sampling_event.html'
    update_form_template = 'selia/components/update/sampling_event.html'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)

        schema = self.object.sampling_event_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form
