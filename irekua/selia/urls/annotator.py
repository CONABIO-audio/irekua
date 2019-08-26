from django.urls import path
from selia.views import annotations


urlpatterns = [
    path(
        'items/detail/<pk>/annotations/add',
        annotations.CollectionItemAnnotatorView.as_view(),
        name='item_annotation_create'),
]
