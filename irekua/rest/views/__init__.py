from .annotations.annotation_tools import AnnotationToolViewSet
from .object_types.annotation_types import AnnotationTypeViewSet
from .object_types.data_collections.collection_types import CollectionTypeViewSet
from .data_collections.collection_devices import CollectionDeviceViewSet
from .data_collections.collection_sites import CollectionSiteViewSet
from .data_collections.collection_users import CollectionUserViewSet
from .devices.device_brands import DeviceBrandViewSet
from .object_types.device_types import DeviceTypeViewSet
from .devices.devices import DeviceViewSet
from .object_types.entailment_types import EntailmentTypeViewSet
from .terms.entailments import EntailmentViewSet
from .object_types.event_types import EventTypeViewSet
from .users.institutions import InstitutionViewSet
from .object_types.item_types import ItemTypeViewSet
from .items import ItemViewSet
from .object_types.licence_types import LicenceTypeViewSet
from .licences import LicenceViewSet
from .metacollections import MetaCollectionViewSet
from .devices.physical_devices import PhysicalDeviceViewSet
from .users.roles import RoleViewSet
from .object_types.sampling_events.sampling_event_types import SamplingEventTypeViewSet
from .sampling_events.sampling_events import SamplingEventViewSet
from .object_types.site_types import SiteTypeViewSet
from .sites import SiteViewSet
from .terms.synonym_suggestions import SynonymSuggestionViewSet
from .terms.synonyms import SynonymViewSet
from .tags import TagViewSet
from .terms.term_suggestions import TermSuggestionViewSet
from .object_types.term_types import TermTypeViewSet
from .terms.terms import TermViewSet
from .users.users import UserViewSet
from .data_collections.data_collections import CollectionViewSet
from .secondary_items import SecondaryItemViewSet
from .annotations.annotations import AnnotationViewSet
from .annotations.annotation_votes import AnnotationVoteViewSet
from .object_types.sampling_events.sampling_event_type_device_types import SamplingEventTypeDeviceTypeViewSet
from .object_types.sampling_events.sampling_event_type_site_types import SamplingEventTypeSiteTypeViewSet
from .sampling_events.sampling_event_devices import SamplingEventDeviceViewSet
from .object_types.data_collections.collection_site_types import CollectionTypeSiteTypeViewSet
from .object_types.data_collections.collection_annotation_types import CollectionTypeAnnotationTypeViewSet
from .object_types.data_collections.collection_administrators import CollectionTypeAdministratorViewSet
from .object_types.data_collections.collection_licence_types import CollectionTypeLicenceTypeViewSet
from .object_types.data_collections.collection_sampling_event_types import CollectionTypeSamplingEventTypeViewSet





__all__ = [
    'AnnotationToolViewSet',
    'AnnotationTypeViewSet',
    'CollectionTypeViewSet',
    'CollectionDeviceViewSet',
    'CollectionSiteViewSet',
    'CollectionUserViewSet',
    'DeviceBrandViewSet',
    'DeviceTypeViewSet',
    'DeviceViewSet',
    'EntailmentTypeViewSet',
    'EntailmentViewSet',
    'EventTypeViewSet',
    'InstitutionViewSet',
    'ItemTypeViewSet',
    'ItemViewSet',
    'LicenceTypeViewSet',
    'LicenceViewSet',
    'MetaCollectionViewSet',
    'PhysicalDeviceViewSet',
    'RoleViewSet',
    'SamplingEventTypeViewSet',
    'SamplingEventViewSet',
    'SiteTypeViewSet',
    'SiteViewSet',
    'SynonymSuggestionViewSet',
    'SynonymViewSet',
    'TagViewSet',
    'TermSuggestionViewSet',
    'TermTypeViewSet',
    'TermViewSet',
    'CollectionViewSet',
    'UserViewSet',
    'SecondaryItemViewSet',
    'AnnotationViewSet',
    'AnnotationVoteViewSet',
    'SamplingEventTypeDeviceTypeViewSet',
    'SamplingEventTypeSiteTypeViewSet',
    'SamplingEventDeviceViewSet',
    'CollectionTypeSiteTypeViewSet',
    'CollectionTypeAdministratorViewSet',
    'CollectionTypeAnnotationTypeViewSet',
    'CollectionTypeLicenceTypeViewSet',
    'CollectionTypeSamplingEventTypeViewSet'
]
