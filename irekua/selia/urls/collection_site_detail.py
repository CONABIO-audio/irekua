from django.urls import path
from selia.views import collection_site_detail


urlpatterns = [
    path(
        'collection_sites/detail/<pk>/',
        collection_site_detail.CollectionSiteDetailView.as_view(),
        name='collection_site_detail'),
    path(
        'collection_sites/detail/<pk>/items/',
        collection_site_detail.CollectionSiteItemsListView.as_view(),
        name='collection_site_items'),
    path(
        'collection_sites/detail/<pk>/items/add',
        collection_site_detail.CollectionSiteItemCreateView.as_view(),
        name='collection_site_item_create'),
]

