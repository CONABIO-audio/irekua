from django.urls import path
from selia.views import collection_detail


urlpatterns = [
    path(
        'collections/detail/<pk>/',
        collection_detail.CollectionDetailView.as_view(),
        name='collection_detail'),
]
