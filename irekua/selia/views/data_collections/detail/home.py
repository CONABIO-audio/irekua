from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Collection


@login_required(login_url='registration:login')
def collection_home(request, collection_name):
    context = {'collection_name': collection_name}
    collection = Collection.objects.get(name=collection_name)

    try:
        context['collection_image'] = collection.logo.url
    except ValueError:
        pass

    return render(request, 'selia/collections/detail/home.html', context)
