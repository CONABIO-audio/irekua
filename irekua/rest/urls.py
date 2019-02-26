from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls


from rest import views


router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'annotations', views.AnnotationViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'sampling_events', views.SamplingEventViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'terms', views.TermViewSet)


urlpatterns = [
    url('', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='Irekua REST API documentation')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
