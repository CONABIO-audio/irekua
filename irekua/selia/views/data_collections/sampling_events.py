from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='registration:login')
def collection_sampling_events(request, collection_name):
    context = {'collection_name': collection_name}
    return render(request, 'selia/collections/sampling_events.html', context)
