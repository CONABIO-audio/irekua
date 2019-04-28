from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    path('upload/', views.upload, name='upload'),
    path('photos/', views.photo_list, name='photo_list'),
    path('photos/upload', views.upload_photo, name='upload_photo'),

    path('user/', views.user_home, name='user_home'),
    path('user/sites/', views.UserSites.as_view(), name='user_sites'),
    path('user/devices/', views.UserDevices.as_view(), name='user_devices'),
    path('user/items/', views.UserItems.as_view(), name='user_items'),
    path('user/sampling_events/', views.UserSamplingEvents.as_view(), name='user_sampling_events'),

    path('collections/', views.user_collections, name='collections'),
    path('collections/open/', views.open_collections, name='open_collections'),

    path(
        'collections/<str:collection_name>/',
        views.collection_home,
        name='collection_home'),
    path(
        'collections/<str:collection_name>/items/',
        views.collection_items,
        name='collection_items'),
    path(
        'collections/<str:collection_name>/devices/',
        views.collection_devices,
        name='collection_devices'),
    path(
        'collections/<str:collection_name>/sites/',
        views.collection_sites,
        name='collection_sites'),
    path(
        'collections/<str:collection_name>/sampling_events/',
        views.collection_sampling_events,
        name='collection_sampling_events'),

    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/',
        views.SamplingEventHome.as_view(),
        name='sampling_event_home'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/',
        views.sampling_event_devices,
        name='sampling_event_devices'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/items/',
        views.sampling_event_items,
        name='sampling_event_items'),

    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/<int:sampling_event_device_id>/',
        views.sampling_event_device,
        name='sampling_event_device'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/<int:sampling_event_device_id>/items/<int:item_id>/',
        views.item,
        name='item'),

    path('about/', views.about, name='about'),

    path('update_session/', views.update_session, name='update_session'),

    path('test/', views.TestView.as_view(), name='test')
]
