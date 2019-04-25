from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import SamplingEvent
from selia.utils import ModelSerializer


class SamplingEventTable(ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = ['id', 'collection', 'started_on', 'ended_on']


@login_required(login_url='registration:login')
def user_sampling_events(request):
    user = request.user
    sampling_events = user.sampling_event_created_by.all()

    table = SamplingEventTable(sampling_events, many=True)
    context = {'table': table}
    return render(request, 'selia/user/sampling_events.html', context)
