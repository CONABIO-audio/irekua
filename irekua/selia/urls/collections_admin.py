from django.urls import path
from selia.views import collections_admin


urlpatterns = [
    path(
        'manage/',
        collections_admin.Home.as_view(),
        name='collections_manager_home'),
    path(
        'manage/managed_collections/',
        collections_admin.ManagedCollectionsView.as_view(),
        name='managed_collections'),
]
