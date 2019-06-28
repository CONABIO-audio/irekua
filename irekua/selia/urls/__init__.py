from django.urls import path
from selia import views

from . import selia
from . import user
from . import data_collections
from . import collections_detail
from . import sampling_event_detail
from . import sampling_event_device_detail
from . import licence_detail

from selia.views.test import test

urlpatterns = (
    selia.urlpatterns +
    user.urlpatterns +
    data_collections.urlpatterns +
    collections_detail.urlpatterns +
    sampling_event_detail.urlpatterns +
    sampling_event_device_detail.urlpatterns +
    licence_detail.urlpatterns
)
