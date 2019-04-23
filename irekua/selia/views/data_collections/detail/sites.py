from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='registration:login')
def collection_sites(request, collection_name):
    context = {'collection_name': collection_name}
    return render(request, 'selia/collections/detail/sites.html', context)
