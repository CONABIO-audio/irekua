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
    path(
        'sampling_events/detail/<pk>/devices/add',
        sampling_event_detail.SamplingEventDeviceCreateView.as_view(),
        name='sampling_event_device_create'),
     path(
        'sampling_events/detail/<pk>/items/add',
        sampling_event_detail.SamplingEventItemCreateView.as_view(),
        name='sampling_event_item_create')   
]

