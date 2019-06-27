from django.urls import path
from selia.views import user


urlpatterns = [
    path('user/', user.user_home, name='user_home'),
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
]
