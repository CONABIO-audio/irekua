from django.urls import path

from . import selia
from . import annotator
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
    annotator.urlpatterns +
    about.urlpatterns +
    create_views.urlpatterns +
    detail_views.urlpatterns +
    list_views.urlpatterns
)
