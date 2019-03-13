from django.conf.urls import url, include
from rest_framework import routers


from rest import views



router = routers.DefaultRouter()
# router.register(r'annotations', views.AnnotationViewSet)
router.register(r'annotation_tools', views.AnnotationToolViewSet)
router.register(r'annotation_types', views.AnnotationTypeViewSet)
# router.register(r'annotation_votes', views.AnnotationVoteViewSet)
# router.register(r'collection_device_types', views.CollectionDeviceTypeViewSet)
# router.register(r'collection_devices', views.CollectionDeviceViewSet)
# router.register(r'collection_roles', views.CollectionRoleViewSet)
# router.register(r'collection_item_types', views.CollectionItemTypeViewSet)
# router.register(r'collections', views.CollectionViewSet)
# router.register(r'collection_types', views.CollectionTypeViewSet)
# router.register(r'collection_sites', views.CollectionSiteViewSet)
# router.register(r'collection_licences', views.CollectionLicenceViewSet)
# router.register(r'collection_users', views.CollectionUserViewSet)
# router.register(r'devices', views.DeviceViewSet)
router.register(r'device_types', views.DeviceTypeViewSet)
router.register(r'device_brands', views.DeviceBrandViewSet)
# router.register(r'entailments', views.EntailmentViewSet)
router.register(r'entailment_types', views.EntailmentTypeViewSet)
router.register(r'event_types', views.EventTypeViewSet)
router.register(r'institutions', views.InstitutionViewSet)
# router.register(r'items', views.ItemViewSet)
# router.register(r'item_types', views.ItemTypeViewSet)
# router.register(r'licences', views.LicenceViewSet)
router.register(r'licence_types', views.LicenceTypeViewSet)
# router.register(r'metacollections', views.MetaCollectionViewSet)
# router.register(r'physical_devices', views.PhysicalDeviceViewSet)
# router.register(r'roles', views.RoleViewSet)
# router.register(r'sampling_events', views.SamplingEventViewSet)
router.register(r'sampling_event_types', views.SamplingEventTypeViewSet)
# router.register(r'secondary_items', views.SecondaryItemViewSet)
# router.register(r'sites', views.SiteViewSet)
router.register(r'site_types', views.SiteTypeViewSet)
# router.register(r'sources', views.SourceViewSet)
# router.register(r'synonyms', views.SynonymViewSet)
# router.register(r'synonym_suggestions', views.SynonymSuggestionViewSet)
# router.register(r'tags', views.TagViewSet)
router.register(r'terms', views.TermViewSet)
router.register(r'term_types', views.TermTypeViewSet)
# router.register(r'term_suggestions', views.TermSuggestionViewSet)
# router.register(r'users', views.UserViewSet)


urlpatterns = [
    url('', include(router.urls)),
]
