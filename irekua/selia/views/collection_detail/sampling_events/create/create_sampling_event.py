from django import forms

from database.models import SamplingEvent

from selia.forms.widgets import BootstrapDateTimePickerInput
from selia.forms.json_field import JsonField
from selia.views.utils import SeliaCreateView


class SamplingEventCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'sampling_event_type',
            'collection_site',
            'metadata',
            'started_on',
            'ended_on',
            'collection'
        ]

        widgets = {
            'started_on': BootstrapDateTimePickerInput(),
            'ended_on': BootstrapDateTimePickerInput(),
        }


class SamplingEventCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/sampling_events/create/create_sampling_event.html'
    model = SamplingEvent
    success_url = 'selia:collection_sampling_events'
    form_class = SamplingEventCreateForm
