from django.urls import path
from selia.views import user


urlpatterns = [
    path('user/', user.UserHomeView.as_view(), name='user_home'),
    path(
        'user/devices/',
        user.UserPhysicalDeviceListView.as_view(),
        name='user_devices'),
    path(
        'user/sites/',
        user.UserSitesListView.as_view(),
        name='user_sites'),
    path(
        'user/items/',
        user.UserItemsListView.as_view(),
        name='user_items'),
    path(
        'user/sampling_events/',
        user.UserSamplingEventsListView.as_view(),
        name='user_sampling_events'),
    path(
        'user/devices/detail/<pk>/',
        user.UserPhysicalDeviceDetailView.as_view(),
        name='user_device_detail'),
    path(
        'user/sites/detail/<pk>/',
        user.UserSiteDetailView.as_view(),
        name='user_site_detail'),
    path(
        'user/items/detail/<pk>/',
        user.UserItemDetailView.as_view(),
        name='user_item_detail'),
    path(
        'user/sampling_events/detail/<pk>/',
        user.UserSamplingEventDetailView.as_view(),
        name='user_sampling_event_detail'),
]
