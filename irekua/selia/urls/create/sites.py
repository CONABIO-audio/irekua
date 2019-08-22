from django.urls import path
from selia.views.create import sites


urlpatterns = [
    path(
        'sites/create/',
        sites.CreateSiteView.as_view(),
        name='create_site'),
]
