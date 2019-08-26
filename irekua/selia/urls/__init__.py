from django.urls import path
from selia import views

from . import selia
from . import item_detail
from . import autocomplete
from . import collections_admin
from . import about

from . import create_views
from . import detail_views
from . import list_views

urlpatterns = (
    selia.urlpatterns +
    autocomplete.urlpatterns +
    collections_admin.urlpatterns +
    item_detail.urlpatterns +
    about.urlpatterns +
    create_views.urlpatterns +
    detail_views.urlpatterns +
    list_views.urlpatterns
)
