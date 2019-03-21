from django.conf.urls import url, include
from rest_framework_nested import routers
# from rest_framework import routers
from rest import views


router = routers.DefaultRouter()
# router.register(r'annotations', views.AnnotationViewSet)
# router.register(r'annotation_votes', views.AnnotationVoteViewSet)
# router.register(r'secondary_items', views.SecondaryItemViewSet)
router.register(r'annotation_tools', views.AnnotationToolViewSet)
router.register(r'annotation_types', views.AnnotationTypeViewSet)
router.register(r'collection_types', views.CollectionTypeViewSet)
router.register(r'collections', views.CollectionViewSet)
router.register(r'device_brands', views.DeviceBrandViewSet)
router.register(r'device_types', views.DeviceTypeViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'entailment_types', views.EntailmentTypeViewSet)
router.register(r'entailments', views.EntailmentViewSet)
router.register(r'event_types', views.EventTypeViewSet)
router.register(r'institutions', views.InstitutionViewSet)
router.register(r'item_types', views.ItemTypeViewSet)
router.register(r'items', views.ItemViewSet, base_name='items')
router.register(r'licence_types', views.LicenceTypeViewSet)
router.register(r'licences', views.LicenceViewSet)
router.register(r'metacollections', views.MetaCollectionViewSet)
router.register(r'physical_devices', views.PhysicalDeviceViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'sampling_event_types', views.SamplingEventTypeViewSet)
router.register(r'sampling_events', views.SamplingEventViewSet)
router.register(r'site_types', views.SiteTypeViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'synonym_suggestions', views.SynonymSuggestionViewSet)
router.register(r'synonyms', views.SynonymViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'term_suggestions', views.TermSuggestionViewSet)
router.register(r'term_types', views.TermTypeViewSet)
router.register(r'terms', views.TermViewSet)
router.register(r'users', views.UserViewSet)

collections_router = routers.NestedSimpleRouter(
    router,
    r'collections',
    lookup='collection')
collections_router.register(
    r'sampling_events',
    views.CollectionSamplingEventViewSet,
    base_name='collection-samplingevents')
collections_router.register(
    r'items',
    views.CollectionItemViewSet,
    base_name='collection-items')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(collections_router.urls)),
]
