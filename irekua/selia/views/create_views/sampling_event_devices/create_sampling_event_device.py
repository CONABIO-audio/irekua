from django import forms
from selia.views.utils import SeliaCreateView

from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import CollectionDevice
from database.models import SamplingEventTypeDeviceType

from selia.forms.json_field import JsonField


class CreateSamplingEventDeviceForm(forms.ModelForm):
    metadata = JsonField()
    configuration = JsonField()

    class Meta:
        model = SamplingEventDevice
        fields = [
            'sampling_event',
            'collection_device',
            'metadata',
            'commentaries',
            'configuration',
            'licence'
        ]


class CreateSamplingEventDeviceView(SeliaCreateView):
    model = SamplingEventDevice
    form_class = CreateSamplingEventDeviceForm

    template_name = 'selia/create/sampling_event_devices/create_form.html'
    success_url = 'selia:sampling_event_devices'

    def get_success_url_args(self):
        return [self.request.GET['sampling_event']]

    def get_additional_query_on_sucess(self):
        sampling_event = self.object.sampling_event
        return {
            'collection': sampling_event.collection.pk,
            'sampling_event': sampling_event.pk,
            'sampling_event_device': self.object.pk
        }

    def get_initial(self):
        self.sampling_event = SamplingEvent.objects.get(
            pk=self.request.GET['sampling_event'])
        self.collection_device = CollectionDevice.objects.get(
            pk=self.request.GET['collection_device'])

        return {
            'sampling_event': self.sampling_event,
            'collection_device': self.collection_device
        }

    def post(self, *args, **kwargs):
        print(self.request.POST)
        return super().post(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.sampling_event.collection
        context['sampling_event'] = self.sampling_event
        context['collection_device'] = self.collection_device

        device = self.collection_device.physical_device.device
        info = SamplingEventTypeDeviceType.objects.get(
            sampling_event_type=self.sampling_event.sampling_event_type,
            device_type=device.device_type)

        context['info'] = info
        context['form'].fields['metadata'].update_schema(
            info.metadata_schema)

        context['form'].fields['configuration'].update_schema(
            device.configuration_schema)
        return context
