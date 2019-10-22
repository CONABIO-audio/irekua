from django.urls import path
from .views import upload
from .views import generate_thumbnail


urlpatterns = [
    path('', upload, name="item_upload"),
    path('thumbnails', generate_thumbnail, name="thumbnails"),
]
