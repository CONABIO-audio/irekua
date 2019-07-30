from django.urls import path
from selia.views import collections_admin


urlpatterns = [
    path(
        'admin/',
        collections_admin.Home.as_view(),
        name='collections_admin_home'),
    path(
        'admin/managed_collections/',
        collections_admin.ManagedCollectionsView.as_view(),
        name='managed_collections'),
]
