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
    path(
        'sampling_events/detail/<pk>/items/',
        sampling_event_detail.SamplingEventItemsListView.as_view(),
        name='sampling_event_items'),
]

