from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

from .additional import additional_router
from .main import main_router
from .object_types import object_types_router

schema_view = get_swagger_view(title='Irekua REST API')


urlpatterns = [
    url(r'^', include(main_router.urls)),
    url(r'^types/', include(object_types_router.urls)),
    url(r'^additional/', include(additional_router.urls)),
    url(r'^swagger-docs/', schema_view)
]
