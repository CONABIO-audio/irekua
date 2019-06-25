from django.urls import path
from selia.views import collection_detail


urlpatterns = [
    path(
        'collections/detail/<pk>/',
        collection_detail.CollectionDetailView.as_view(),
        name='collection_detail'),
    path(
        'collections/detail/<pk>/devices/',
        collection_detail.CollectionDevicesListView.as_view(),
        name='collection_devices'),
    path(
        'collections/detail/<pk>/sampling_events/',
        collection_detail.CollectionSamplingEventListView.as_view(),
        name='collection_sampling_events'),
    path(
        'collections/detail/<pk>/sites/',
        collection_detail.CollectionSitesListView.as_view(),
        name='collection_sites'),
    path(
        'collections/detail/<pk>/items/',
        collection_detail.CollectionItemsListView.as_view(),
        name='collection_items'),
    path(
        'collections/devices/<pk>/',
        collection_detail.CollectionDeviceDetailView.as_view(),
        name='collection_device_detail'),
    path(
        'collections/sites/<pk>/',
        collection_detail.CollectionSiteDetailView.as_view(),
        name='collection_site_detail'),
]
