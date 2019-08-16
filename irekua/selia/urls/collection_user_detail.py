from django.urls import path
from selia.views import collection_detail


urlpatterns = [
    path(
        'collection_user/detail/<pk>/',
        collection_detail.CollectionUserDetailView.as_view(),
        name='collection_user_detail'),
]
