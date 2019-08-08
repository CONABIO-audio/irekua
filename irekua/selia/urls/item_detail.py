from django.urls import path
from selia.views import item_detail


urlpatterns = [
    path(
        'items/detail/<pk>/',
        item_detail.CollectionItemDetailView.as_view(),
        name='item_detail'),
    path(
        'items/detail/<pk>/annotations/add',
        item_detail.CollectionItemAnnotatorView.as_view(),
        name='item_annotation_create'),
    path(
        'items/detail/<pk>/annotations/',
        item_detail.CollectionAnnotationsListView.as_view(),
        name='item_annotations')

]
