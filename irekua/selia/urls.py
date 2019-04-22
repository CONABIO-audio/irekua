from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('user/', views.user_home, name='user_home'),
    path('user/collections/', views.user_collections, name='user_collections'),
    path('user/sites/', views.user_sites, name='user_sites'),
    path('user/devices/', views.user_devices, name='user_devices'),
    path('user/items/', views.user_items, name='user_items'),
    path('user/sampling_events/', views.user_sampling_events, name='user_sampling_events'),

    path(
        'collections/<str:collection_name>/',
        views.collection_home,
        name='collection_home'),
    path(
        'collections/<str:collection_name>/items',
        views.collection_items,
        name='collection_items'),
    path(
        'collections/<str:collection_name>/devices',
        views.collection_devices,
        name='collection_devices'),
    path(
        'collections/<str:collection_name>/sites',
        views.collection_sites,
        name='collection_sites'),
    path(
        'collections/<str:collection_name>/sampling_events',
        views.collection_sampling_events,
        name='collection_sampling_events'),

    path(
        'collections/<str:collection_name>/<int:sampling_event_id>/',
        views.sampling_event_home,
        name='sampling_event_home'),
    path(
        'collections/<str:collection_name>/<int:sampling_event_id>/devices',
        views.sampling_event_devices,
        name='sampling_event_devices'),
    path(
        'collections/<str:collection_name>/<int:sampling_event_id>/items',
        views.sampling_event_items,
        name='sampling_event_items'),

    path(
        'collections/<str:collection_name>/<int:sampling_event_id>/<int:sampling_event_device_id>/',
        views.sampling_event_device,
        name='sampling_event_device'),
    path(
        'collections/<str:collection_name>/<int:sampling_event_id>/<int:sampling_event_device_id>/<int:item_id>',
        views.item,
        name='item'),

    path('about/', views.about, name='about'),
]
