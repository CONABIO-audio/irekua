from django.urls import path
from selia.views import licence_detail


urlpatterns = [
    path(
        'licences/detail/<pk>/',
        licence_detail.LicenceDetailView.as_view(),
        name='licence_detail'),
]
