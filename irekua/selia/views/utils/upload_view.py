from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from database.models import SamplingEventDevice, Licence
from .create_base import SeliaCreateView

class SeliaUploadItemsView(SeliaCreateView):
    def handle_create(self):
    	form = self.get_form()
    	if form.is_valid();
    		
    def get_initial(self):
        sampling_event_device_pk = None
        licence_pk = None

        if "sampling_event_device" in self.request.GET:
        	sampling_event_device_pk = self.request.GET["sampling_event_device"]

        if "licence":
        	licence_pk = self.request.GET["licence"]

        sampling_event_device = SamplingEventDevice.objects.get_object_or_404(pk=sampling_event_device_pk)
        licence = Licence.objects.get_object_or_404(pk=licence_pk)

        initial = {
        	'collection' : sampling_event_device.collection_device.collection,
            'sampling_event': sampling_event_device.sampling_event,
            'sampling_event_device': sampling_event_device,
            'licence': licence
        }
         
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sampling_event_device_pk = None
        licence_pk = None

        if "sampling_event_device" in self.request.GET:
        	sampling_event_device_pk = self.request.GET["sampling_event_device"]

        if "licence":
        	licence_pk = self.request.GET["licence"]

        sampling_event_device = SamplingEventDevice.objects.get_object_or_404(pk=sampling_event_device_pk)
        context["sampling_event_device"] = sampling_event_device
        context["sampling_event"] = sampling_event_device.sampling_event
        context["licence"] = Licence.objects.get_object_or_404(pk=licence_pk)

        return context