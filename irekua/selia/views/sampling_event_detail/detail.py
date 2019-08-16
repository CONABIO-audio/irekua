from django.views.generic.detail import SingleObjectMixin
from django import forms

from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField
from selia.forms.widgets import BootstrapDateTimePickerInput
from database.models import SamplingEvent


class SamplingEventUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'started_on',
            'ended_on',
            'commentaries',
            'metadata',
        ]

        widgets = {
            'started_on': BootstrapDateTimePickerInput(),
            'ended_on': BootstrapDateTimePickerInput(),
        }


class SamplingEventDetailView(SeliaDetailView):
    model = SamplingEvent
    form_class = SamplingEventUpdateForm
    delete_redirect_url = 'selia:collection_sampling_events'

    template_name = 'selia/sampling_event_detail/detail.html'
    help_template = 'selia/components/help/collection_sampling_events.html'
    summary_template = 'selia/components/summaries/sampling_event.html'
    detail_template = 'selia/components/details/sampling_event.html'
    update_form_template = 'selia/components/update/sampling_event.html'

    def get_delete_redirect_url_args(self):
        return [self.object.collection.pk]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        schema = self.object.sampling_event_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sampling_event = self.object
        context['sampling_event'] = sampling_event
        return context
