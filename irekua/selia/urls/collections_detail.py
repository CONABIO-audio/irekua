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
        'collections/detail/<pk>/licences/',
        collection_detail.CollectionLicencesListView.as_view(),
        name='collection_licences'),
    path(
        'collections/detail/<pk>/items/',
        collection_detail.CollectionItemsListView.as_view(),
        name='collection_items'),
    path(
        'collections/detail/<pk>/users/',
        collection_detail.CollectionUserListView.as_view(),
        name='collection_users'),
    path(
        'collections/detail/<pk>/items/add/',
        collection_detail.CollectionItemCreateView.as_view(),
        name='collection_item_create'),
    path(
        'collections/detail/<pk>/devices/add/',
        collection_detail.CollectionDeviceCreateView.as_view(),
        name='collection_device_create'),
    # path(
    #     'collections/detail/<pk>/sampling_events/add/',
    #     collection_detail.SamplingEventCreateView.as_view(),
    #     name='collection_sampling_event_create'),
    path(
        'collections/detail/<pk>/extra/physical_device/create/',
        collection_detail.PhysicalDeviceCreateView.as_view(),
        name='physical_device_create'),
    path(
        'collections/detail/<pk>/sites/add/',
        collection_detail.CollectionSiteCreateView.as_view(),
        name='collection_site_create'),
    path(
        'collections/detail/<pk>/licences/add/',
        collection_detail.CollectionLicenceCreateView.as_view(),
        name='collection_licence_create'),
    path(
        'collections/detail/<pk>/users/add/',
        collection_detail.CollectionUserCreateView.as_view(),
        name='collection_user_create'),
]
