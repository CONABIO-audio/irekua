from django.urls import path
from selia.views import sampling_event_device_detail


urlpatterns = [
    path(
        'sampling_event_devices/detail/<pk>/',
        sampling_event_device_detail.SamplingEventDeviceDetailView.as_view(),
        name='sampling_event_device_detail'),
]
