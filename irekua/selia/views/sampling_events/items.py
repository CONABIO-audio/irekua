from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='registration:login')
def sampling_event_items(request, collection_name, sampling_event_id):
    context = {
        'collection_name': collection_name,
        'sampling_event_id': sampling_event_id
    }
    return render(request, 'selia/sampling_events/items.html', context)
