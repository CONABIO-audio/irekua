from django.urls import path
from selia.views import about


urlpatterns = [
    path('about/', about.about_selia, name='about'),
    path('about/irekua/', about.about_irekua, name='about_irekua'),
    path('about/contact/', about.about_contact, name='contact'),
    path('collections/', about.about_collections, name='about_collections')
]
