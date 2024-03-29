import json
import pytz
from timezonefinder import TimezoneFinder

from django import forms
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse
from django.http import HttpResponse

from rest.serializers.object_types.data_collections.items import ListSerializer

from database.models import Item, SamplingEventDevice, Licence, CollectionItemType
from database.models import Item
from database.models import SamplingEventDevice
from database.models import Licence

from selia.views.create_views.create_base import SeliaCreateView
from irekua_utils.permissions.items import (
        items as item_permissions)


class ItemUploadView(SeliaCreateView):
    model = Item
    template_name = 'selia/create/items/upload.html'
    success_url = 'selia:collection_items'
    fields = [
        "item_type",
        "item_file",
        "sampling_event_device",
        "source",
        "captured_on",
        "captured_on_year",
        "captured_on_month",
        "captured_on_day",
        "captured_on_hour",
        "captured_on_minute",
        "captured_on_second",
        "captured_on_timezone",
        "licence",
        "tags"
    ]

    def form_valid(self, form):
        upload_result = {
            "result_type": "unknown",
            "result": {}
        }

        item = form.save(commit=False)
        item.created_by = self.request.user

        try:
            item.save()
            upload_result["result_type"] = "success"
            upload_result["result"]["item"] = {
                "pk": item.pk,
                "created_on": str(item.created_on),
                "captured_on": str(item.captured_on),
                "captured_on_year": str(item.captured_on_year),
                "captured_on_month": str(item.captured_on_month),
                "captured_on_day": str(item.captured_on_day),
                "captured_on_hour": str(item.captured_on_hour),
                "captured_on_minute": str(item.captured_on_minute),
                "captured_on_second": str(item.captured_on_second),
                "detail_url": reverse("selia:item_detail", args=[item.pk]),
                "url": item.item_file.url
            }

        except:
            duplicate = Item.objects.filter(hash=item.hash)

            if duplicate:
                upload_result["result_type"] = "duplicate"
                upload_result["result"]["item"] = {
                    "pk": duplicate[0].pk,
                    "created_on": str(duplicate[0].created_on),
                    "captured_on": str(item.captured_on),
                    "captured_on_year": str(item.captured_on_year),
                    "captured_on_month": str(item.captured_on_month),
                    "captured_on_day": str(item.captured_on_day),
                    "captured_on_hour": str(item.captured_on_hour),
                    "captured_on_minute": str(item.captured_on_minute),
                    "captured_on_second": str(item.captured_on_second),
                    "detail_url": reverse("selia:item_detail", args=[duplicate[0].pk]),
                    "url": duplicate[0].item_file.url
                }

            return HttpResponse(
                json.dumps(upload_result),
                content_type="application/json",
                status=400)

        return HttpResponse(
            json.dumps(upload_result),
            content_type="application/json",
            status=200)

    def form_invalid(self, form):
        upload_result = {
            "result_type": "invalid_form",
            "result": form.errors
        }

        return HttpResponse(
            json.dumps(upload_result),
            content_type="application/json",
            status=400)

    def get_initial(self):
        sampling_event_device_pk = None
        licence_pk = None

        if "sampling_event_device" in self.request.GET:
            sampling_event_device_pk = self.request.GET["sampling_event_device"]

        if "licence":
            licence_pk = self.request.GET["licence"]

        sampling_event_device = get_object_or_404(
            SamplingEventDevice, pk=sampling_event_device_pk)
        licence = get_object_or_404(Licence, pk=licence_pk)

        initial = {
            'sampling_event_device': sampling_event_device,
            'licence': licence,
        }

        return initial

    def get_item_types(self,sampling_event_device):
        collection_item_types = CollectionItemType.objects.filter(
            collection_type=sampling_event_device.collection_device.collection.collection_type,
            item_type__mime_types__in=sampling_event_device.collection_device.physical_device.device.device_type.mime_types.all()).distinct()

        serialized = ListSerializer(collection_item_types, many=True, context={'request':self.request})
        return json.dumps(serialized.data)

    def get_site_tz_info(self,site):
        tf = TimezoneFinder()
        timezone = tf.certain_timezone_at(lng=site.longitude,lat=site.latitude)
        return json.dumps({"site_timezone":timezone,"tz_list":pytz.all_timezones})

    def get_objects(self):
        if not hasattr(self, 'sampling_event_device'):
            if "sampling_event_device" in self.request.GET:
                sampling_event_device_pk = self.request.GET["sampling_event_device"]

            self.sampling_event_device = get_object_or_404(
                SamplingEventDevice, pk=sampling_event_device_pk)

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.create(user,
            sampling_event_device=self.sampling_event_device)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sampling_event_device_pk = None
        licence_pk = None

        if "sampling_event_device" in self.request.GET:
            sampling_event_device_pk = self.request.GET["sampling_event_device"]

        if "licence":
            licence_pk = self.request.GET["licence"]

        sampling_event_device = self.sampling_event_device
        licence = get_object_or_404(Licence, pk=licence_pk)

        context["collection"] = sampling_event_device.collection_device.collection
        context["sampling_event_device"] = sampling_event_device
        context["sampling_event"] = sampling_event_device.sampling_event
        context["licence"] = licence
        context["started_on"] = sampling_event_device.sampling_event.started_on.strftime('%Y-%m-%d %H:%M:%S');
        context["ended_on"] = sampling_event_device.sampling_event.ended_on.strftime('%Y-%m-%d %H:%M:%S');
        context["item_types"] = self.get_item_types(sampling_event_device)
        context["tz_info"] = self.get_site_tz_info(sampling_event_device.sampling_event.collection_site.site)

        return context
