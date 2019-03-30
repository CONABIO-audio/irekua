from django.conf.urls import url, include
from rest_framework_nested import routers
# from rest_framework import routers
from rest import views


router = routers.DefaultRouter()
# router.register(r'annotations', views.AnnotationViewSet)
# router.register(r'annotation_votes', views.AnnotationVoteViewSet)
# router.register(r'secondary_items', views.SecondaryItemViewSet)
router.register(
    r'annotation_tools',
    views.AnnotationToolViewSet,
    basename='annotationtool')
router.register(
    r'annotation_types',
    views.AnnotationTypeViewSet,
    basename='annotationtype')
router.register(
    r'collection_types',
    views.CollectionTypeViewSet,
    basename='collectiontype')
router.register(
    r'collection_devices',
    views.CollectionDeviceViewSet,
    basename='collectiondevice')
router.register(
    r'collection_sites',
    views.CollectionSiteViewSet,
    basename='collectionsite')
router.register(
    r'collection_users',
    views.CollectionUserViewSet,
    basename='collectionuser')
router.register(
    r'collections',
    views.CollectionViewSet,
    basename='collection')
router.register(
    r'device_brands',
    views.DeviceBrandViewSet,
    basename='devicebrand')
router.register(
    r'device_types',
    views.DeviceTypeViewSet,
    basename='devicetype')
router.register(
    r'devices',
    views.DeviceViewSet,
    basename='device')
router.register(
    r'entailment_types',
    views.EntailmentTypeViewSet,
    basename='entailmenttype')
router.register(
    r'entailments',
    views.EntailmentViewSet,
    basename='entailment')
router.register(
    r'event_types',
    views.EventTypeViewSet,
    basename='eventtype')
router.register(
    r'institutions',
    views.InstitutionViewSet,
    basename='institution')
router.register(
    r'item_types',
    views.ItemTypeViewSet,
    basename='itemtype')
router.register(
    r'items',
    views.ItemViewSet,
    basename='item')
router.register(
    r'licence_types',
    views.LicenceTypeViewSet,
    basename='licencetype')
router.register(
    r'licences',
    views.LicenceViewSet,
    basename='licence')
router.register(
    r'metacollections',
    views.MetaCollectionViewSet,
    basename='metacollection')
router.register(
    r'physical_devices',
    views.PhysicalDeviceViewSet,
    basename='physicaldevice')
router.register(
    r'roles',
    views.RoleViewSet,
    basename='role')
router.register(
    r'sampling_event_types',
    views.SamplingEventTypeViewSet,
    basename='samplingeventtype')
router.register(
    r'sampling_events',
    views.SamplingEventViewSet,
    basename='samplingevent')
router.register(
    r'site_types',
    views.SiteTypeViewSet,
    basename='sitetype')
router.register(
    r'sites',
    views.SiteViewSet,
    basename='site')
router.register(
    r'synonym_suggestions',
    views.SynonymSuggestionViewSet,
    basename='synonymsuggestion')
router.register(
    r'synonyms',
    views.SynonymViewSet,
    basename='synonym')
router.register(
    r'tags',
    views.TagViewSet,
    basename='tag')
router.register(
    r'term_suggestions',
    views.TermSuggestionViewSet,
    basename='termsuggestion')
router.register(
    r'term_types',
    views.TermTypeViewSet,
    basename='termtype')
router.register(
    r'terms',
    views.TermViewSet,
    basename='term')
router.register(
    r'users',
    views.UserViewSet,
    basename='user')


urlpatterns = [
    url(r'^', include(router.urls)),
]
