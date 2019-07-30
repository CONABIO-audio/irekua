from django.urls import path
from selia.views import sampling_event_device_detail


urlpatterns = [
    path(
        'sampling_event_devices/detail/<pk>/',
        sampling_event_device_detail.SamplingEventDeviceDetailView.as_view(),
        name='sampling_event_device_detail'),
    path(
        'sampling_event_devices/detail/<pk>/items/',
        sampling_event_device_detail.SamplingEventDeviceItemsListView.as_view(),
        name='sampling_event_device_items'),
    path(
        'sampling_event_devices/detail/<pk>/items/add',
        sampling_event_device_detail.SamplingEventDeviceItemCreateView.as_view(),
        name='sampling_event_device_item_create')
]
