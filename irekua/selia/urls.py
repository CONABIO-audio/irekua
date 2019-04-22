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
    path('about/', views.about, name='about'),
]
