from django.urls import path
from selia import views

from . import selia
from . import user
from . import data_collections
from . import collections_detail


urlpatterns = (
    selia.urlpatterns +
    user.urlpatterns +
    data_collections.urlpatterns +
    collections_detail.urlpatterns
)
