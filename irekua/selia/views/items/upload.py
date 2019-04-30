from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms

from database import models



def handle_files(files, sampling_event_device):
    collection_type = sampling_event_device.sampling_event.collection.collection_type

    if collection_type.restrict_item_types:
        queryset = collection_type.item_types.all()
    else:
        queryset = models.ItemType.objects.all()

    for tempfile in files:
        possible_types = queryset.filter(media_type=tempfile.content_type)
        print(possible_types.count())


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


def upload_items(request, collection_name, sampling_event_id, sampling_event_device_id):
    if request.method == "POST":
        sampling_event_device = models.SamplingEventDevice.objects.get(
            pk=sampling_event_device_id)
        handle_files(request.FILES.getlist('file_field'), sampling_event_device)
        return HttpResponseRedirect('#')

    context = {
        'form': FileFieldForm(),
        'collection_name': collection_name,
        'sampling_event_id': sampling_event_id,
        'sampling_event_device_id': sampling_event_device_id
    }
    return render(request, 'selia/items/upload.html', context)
