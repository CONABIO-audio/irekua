from django.urls import path
from selia.views import item_detail


urlpatterns = [
    path(
        'items/detail/<pk>/',
        item_detail.CollectionItemDetailView.as_view(),
        name='item_detail'),
]
