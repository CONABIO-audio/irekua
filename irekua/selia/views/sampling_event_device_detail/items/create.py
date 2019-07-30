from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaMultipleItemsCreateView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import Item

class SamplingEventDeviceItemCreateView(SeliaMultipleItemsCreateView):
    template_name = 'selia/sampling_event_device_detail/items/create.html'
    model = Item
    success_url = 'selia:sampling_event_device_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]

    def get_success_url_args(self):
        return [self.kwargs['pk']]
        
    def get_initial(self):
        initial = {
            'sampling_event_device': SamplingEventDevice.objects.get(pk=self.kwargs['pk'])
        }

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event_device'] = self.get_object(queryset=SamplingEventDevice.objects.all())

        return context
