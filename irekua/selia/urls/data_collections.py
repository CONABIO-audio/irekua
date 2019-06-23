from django.urls import path
from selia.views import data_collections


urlpatterns = [
    path(
        'collections/',
        data_collections.AboutCollectionsView.as_view(),
        name='collections_about'),
    path(
        'collections/user',
        data_collections.UserCollectionsView.as_view(),
        name='collections_user'),
    path(
        'collections/open',
        data_collections.OpenCollectionsView.as_view(),
        name='collections_open'),
]
