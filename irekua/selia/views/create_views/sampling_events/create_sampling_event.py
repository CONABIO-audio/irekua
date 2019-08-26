from django import forms

from database.models import SamplingEvent
from database.models import SamplingEventType
from database.models import Collection
from database.models import CollectionSite

from selia.forms.widgets import BootstrapDateTimePickerInput
from selia.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView


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
    model = SamplingEvent
    form_class = SamplingEventCreateForm

    success_url = 'selia:collection_sampling_events'
    template_name = 'selia/create/sampling_events/create_form.html'

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_additional_query_on_sucess(self):
        return {
            'collection': self.object.collection.pk,
            'sampling_event': self.object.pk
        }

    def get_initial(self):
        self.collection = Collection.objects.get(
            pk=self.request.GET['collection'])
        self.collection_site = CollectionSite.objects.get(
            pk=self.request.GET['collection_site'])
        self.sampling_event_type = SamplingEventType.objects.get(
            pk=self.request.GET['sampling_event_type'])

        return {
            'collection': self.collection,
            'collection_site': self.collection_site,
            'sampling_event_type': self.sampling_event_type,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['collection_site'] = self.collection_site
        context['sampling_event_type'] = self.sampling_event_type

        context['form'].fields['metadata'].update_schema(
            self.sampling_event_type.metadata_schema)
        return context
