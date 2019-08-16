from django.urls import path
from selia import views

from . import selia
from . import user
from . import data_collections
from . import collections_detail
from . import sampling_event_detail
from . import sampling_event_device_detail
from . import licence_detail
from . import collection_site_detail
from . import collection_device_detail
from . import item_detail
from . import autocomplete
from . import collections_admin
from . import about
from . import collection_user_detail

urlpatterns = (
    selia.urlpatterns +
    user.urlpatterns +
    data_collections.urlpatterns +
    collections_detail.urlpatterns +
    sampling_event_detail.urlpatterns +
    sampling_event_device_detail.urlpatterns +
    licence_detail.urlpatterns +
    collection_site_detail.urlpatterns +
    collection_device_detail.urlpatterns +
    autocomplete.urlpatterns +
    collections_admin.urlpatterns +
    item_detail.urlpatterns +
    about.urlpatterns +
    collection_user_detail.urlpatterns
)
