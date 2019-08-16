from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaCreateView

from irekua_utils.filters.data_collections import collection_devices as device_utils

from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import CollectionDevice
from selia.views.utils import SeliaList


class CreateSamplingEventDeviceForm(forms.ModelForm):
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


class SamplingEventDeviceCreateView(SeliaCreateView):
    template_name = 'selia/sampling_event_detail/devices/create.html'
    model = SamplingEventDevice
    success_url = 'selia:sampling_event_devices'
    form_class = CreateSamplingEventDeviceForm

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def get_back_url(self):
        if 'back' in self.request.GET:
            chain_str = self.get_chain()
            return self.request.GET['back']+"?sampling_event="+self.kwargs['pk']+"&chain="+chain_str
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()

            return next_url+"?sampling_event="+self.kwargs['pk']+"&chain="+chain_str

    def handle_finish_create(self):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?sampling_event="+self.kwargs['pk']+"&chain="+chain_str

        return redirect(redirect_url)


    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            sampling_event_device = form.save(commit=False)
            sampling_event_device.created_by = self.request.user
            sampling_event_device.save()
            return self.handle_finish_create()

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_initial(self):
        sampling_event = SamplingEvent.objects.get(pk=self.kwargs['pk'])
        initial = {
            'sampling_event': sampling_event
        }

        if 'collection_device' in self.request.GET:
            initial['collection_device'] = CollectionDevice.objects.get(pk=self.request.GET['collection_device'])

        return initial

    def get_device_list_context(self):
        queryset_ = self.sampling_event.collection.collectiondevice_set.all()

        class DeviceList(SeliaList):
            prefix = 'device_list'

            filter_class = device_utils.Filter
            search_fields = device_utils.search_fields
            ordering_fields = device_utils.ordering_fields

            queryset = queryset_

            list_item_template = 'selia/components/select_list_items/collection_devices.html'
            filter_form_template = 'selia/components/filters/collection_device.html'

        site_list = DeviceList()
        return site_list.get_context_data(self.request)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        self.sampling_event = self.get_object(queryset=SamplingEvent.objects.all())
        context['sampling_event'] = self.sampling_event
        context['collection_device_list'] = self.get_device_list_context()

        if 'collection_device' in self.request.GET:
            collection_device = CollectionDevice.objects.get(pk=self.request.GET['collection_device'])
            context['collection_device'] = collection_device

        return context
