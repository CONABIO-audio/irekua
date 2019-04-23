from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Collection
from database.models import CollectionDevice
from selia.utils import ModelTable


class DevicesTable(ModelTable):
    class Meta:
        model = CollectionDevice
        fields = ['id', 'physical_device', 'internal_id']


@login_required(login_url='registration:login')
def collection_devices(request, collection_name):
    collection = Collection.objects.get(pk=collection_name)
    queryset = collection.collectiondevice_set.all()

    table = DevicesTable(queryset, many=True)

    context = {'collection_name': collection_name, 'table': table}
    return render(request, 'selia/collections/detail/devices.html', context)
