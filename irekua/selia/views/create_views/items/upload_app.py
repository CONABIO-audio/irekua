from django import forms
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse

from django.http import HttpResponse
from database.models import Item, SamplingEventDevice, Licence
from selia.views.create_views.create_base import SeliaCreateView
import json

class ItemUploadView(SeliaCreateView):
    model = Item
    template_name = 'selia/create/items/upload.html'
    success_url = 'selia:collection_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]   
    
    def handle_upload(self):
        upload_result = {"result_type":"unknown","result":{}}
        form = self.get_form()
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = self.request.user

            try:
                item.save()
                upload_result["result_type"] = "success"
                upload_result["result"]["item"] = {
                         "pk" : item.pk,
                         "created_on" : str(item.created_on),
                         "captured_on" : str(item.captured_on),
                         "detail_url" : reverse("selia:item_detail", args=[item.pk]),
                         "url" : item.item_file.url
                }

            except:
                duplicate = Item.objects.filter(hash=item.hash)

                if duplicate:
                    upload_result["result_type"] = "duplicate"
                    upload_result["result"]["item"] = {
                             "pk" : duplicate[0].pk,
                             "created_on" : str(duplicate[0].created_on),
                             "captured_on" : str(duplicate[0].captured_on),
                             "detail_url" : reverse("selia:item_detail", args=[duplicate[0].pk]),
                             "url" : duplicate[0].item_file.url
                    }

            
        else:
            upload_result["result_type"] = "invalid_form"
            upload_result["result"] = form.errors

        return HttpResponse(json.dumps(upload_result), content_type="application/json",status=400)

    def post(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return self.handle_upload()

    def get_initial(self):
        sampling_event_device_pk = None
        licence_pk = None

        if "sampling_event_device" in self.request.GET:
            sampling_event_device_pk = self.request.GET["sampling_event_device"]

        if "licence":
            licence_pk = self.request.GET["licence"]

        sampling_event_device = get_object_or_404(SamplingEventDevice,pk=sampling_event_device_pk)
        licence = get_object_or_404(Licence,pk=licence_pk)

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

        sampling_event_device = get_object_or_404(SamplingEventDevice,pk=sampling_event_device_pk)
        licence = get_object_or_404(Licence,pk=licence_pk)
        
        context["collection"] = sampling_event_device.collection_device.collection
        context["sampling_event_device"] = sampling_event_device
        context["sampling_event"] = sampling_event_device.sampling_event
        context["licence"] = licence

        return context


