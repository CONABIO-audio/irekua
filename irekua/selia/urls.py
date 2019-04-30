from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('upload/', views.upload, name='upload'),
    path('photos/', views.photo_list, name='photo_list'),
    path('photos/upload', views.upload_photo, name='upload_photo'),
    path('photos/<int:pk>/', views.delete_photo, name='delete_photo'),

    path('user/', views.user_home, name='user_home'),
    path('user/sites/', views.UserSites.as_view(), name='user_sites'),
    path('user/devices/', views.UserDevices.as_view(), name='user_devices'),
    path('user/items/', views.UserItems.as_view(), name='user_items'),
    path('user/sampling_events/', views.UserSamplingEvents.as_view(), name='user_sampling_events'),

    path('collections/', views.UserCollections.as_view(), name='collections'),
    path('collections/open/', views.OpenCollections.as_view(), name='open_collections'),

    path(
        'collections/<str:collection_name>/',
        views.CollectionHome.as_view(),
        name='collection_home'),
    path(
        'collections/<str:collection_name>/items/',
        views.CollectionItems.as_view(),
        name='collection_items'),
    path(
        'collections/<str:collection_name>/devices/',
        views.CollectionDevices.as_view(),
        name='collection_devices'),
    path(
        'collections/<str:collection_name>/sites/',
        views.CollectionSites.as_view(),
        name='collection_sites'),
    path(
        'collections/<str:collection_name>/sampling_events/',
        views.CollectionSamplingEvents.as_view(),
        name='collection_sampling_events'),

    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/',
        views.SamplingEventHome.as_view(),
        name='sampling_event_home'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/',
        views.SamplingEventDevices.as_view(),
        name='sampling_event_devices'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/items/',
        views.SamplingEventItems.as_view(),
        name='sampling_event_items'),

    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/<int:sampling_event_device_id>/',
        views.SamplingEventDeviceHome.as_view(),
        name='sampling_event_device_home'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/<int:sampling_event_device_id>/items/',
        views.SamplingEventDeviceItems.as_view(),
        name='sampling_event_device_items'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/<int:sampling_event_device_id>/items/<int:item_id>/',
        views.item,
        name='item'),
    path(
        'collections/<str:collection_name>/sampling_events/<int:sampling_event_id>/devices/<int:sampling_event_device_id>/upload',
        views.upload_items, name='upload_items'),

    path('items/gallery/', views.gallery, name='gallery'),
    path('items/annotate/', views.annotate, name='annotate'),

    path('admin/', views.admin_home, name='admin_home'),

    path('about/', views.about, name='about'),

    path('update_session/', views.update_session, name='update_session'),

    path('test/', views.TestView.as_view(), name='test'),

    path('widgets/update_form/<str:model_name>/<str:id>/',views.UserFormCreator,
        name='user_form_creator')
]
