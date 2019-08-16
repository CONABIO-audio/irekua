from django.urls import path
from selia.views import collection_device_detail


urlpatterns = [
    path(
        'collection_devices/detail/<pk>/',
        collection_device_detail.CollectionDeviceDetailView.as_view(),
        name='collection_device_detail'),
    path(
        'collection_devices/detail/<pk>/items/',
        collection_device_detail.CollectionDeviceItemsListView.as_view(),
        name='collection_device_items'),
    path(
        'collection_devices/detail/<pk>/items/add',
        collection_device_detail.CollectionDeviceItemCreateView.as_view(),
        name='collection_device_item_create'),
]
