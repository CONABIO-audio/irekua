from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Collection
from database.models import SamplingEvent
from selia.utils import ModelSerializer


class SamplingEventTable(ModelSerializer):
    with_link = True
    detail_view = 'selia:sampling_event_home'
    url_args = ['id']

    class Meta:
        model = SamplingEvent
        fields = ['id', 'started_on', 'ended_on']


@login_required(login_url='registration:login')
def collection_sampling_events(request, collection_name):
    collection = Collection.objects.get(pk=collection_name)
    queryset = collection.samplingevent_set.all()

    table = SamplingEventTable(queryset, many=True, pre_args=[collection_name])

    context = {'collection_name': collection_name, 'table': table}
    return render(request, 'selia/collections/detail/sampling_events.html', context)
