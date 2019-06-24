from django.urls import path
from selia.views import sampling_event_detail


urlpatterns = [
    path(
        'sampling_events/detail/<pk>/',
        sampling_event_detail.SamplingEventDetailView.as_view(),
        name='sampling_event_detail'),
    path(
        'sampling_events/detail/<pk>/devices/',
        sampling_event_detail.SamplingEventDevicesListView.as_view(),
        name='sampling_event_devices'),
]

