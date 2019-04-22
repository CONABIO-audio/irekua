from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='registration:login')
def item(request, collection_name, sampling_event_id, sampling_event_device_id):
    return render(request, 'selia/sampling_event_devices/item.html')
