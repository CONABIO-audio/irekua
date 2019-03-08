from .annotation_tools import AnnotationToolViewSet
from .annotation_types import AnnotationTypeViewSet
from .annotation_votes import AnnotationVoteViewSet
from .annotations import AnnotationViewSet
from .collection_device_types import CollectionDeviceTypeViewSet
from .collection_devices import CollectionDeviceViewSet
from .collection_item_types import CollectionItemTypeViewSet
from .collection_roles import CollectionRoleViewSet
from .collection_sites import CollectionSiteViewSet
from .collection_licences import CollectionLicenceViewSet
from .collection_types import CollectionTypeViewSet
from .collection_users import CollectionUserViewSet
from .data_collections import CollectionViewSet
from .device_brands import DeviceBrandViewSet
from .device_types import DeviceTypeViewSet
from .devices import DeviceViewSet
from .entailments import EntailmentViewSet
from .entailment_types import EntailmentTypeViewSet
from .event_types import EventTypeViewSet
from .institutions import InstitutionViewSet
from .item_types import ItemTypeViewSet
from .items import ItemViewSet
from .licence_types import LicenceTypeViewSet
from .licences import LicenceViewSet
from .metacollections import MetaCollectionViewSet
from .physical_devices import PhysicalDeviceViewSet
from .roles import RoleViewSet
from .sampling_events import SamplingEventViewSet
from .sampling_event_types import SamplingEventTypeViewSet
from .schemas import SchemaViewSet
from .secondary_items import SecondaryItemViewSet
from .site_types import SiteTypeViewSet
from .sites import SiteViewSet
from .sources import SourceViewSet
from .synonym_suggestions import SynonymSuggestionViewSet
from .synonyms import SynonymViewSet
from .tags import TagViewSet
from .term_suggestions import TermSuggestionViewSet
from .term_types import TermTypeViewSet
from .terms import TermViewSet
from .users import UserViewSet


__all__ = [
    'AnnotationViewSet',
    'AnnotationToolViewSet',
    'AnnotationTypeViewSet',
    'AnnotationVoteViewSet',
    'CollectionViewSet',
    'CollectionDeviceViewSet',
    'CollectionDeviceTypeViewSet',
    'CollectionItemTypeViewSet',
    'CollectionRoleViewSet',
    'CollectionSiteViewSet',
    'CollectionLicenceViewSet',
    'CollectionTypeViewSet',
    'CollectionUserViewSet',
    'DeviceViewSet',
    'DeviceBrandViewSet',
    'DeviceTypeViewSet',
    'EntailmentViewSet',
    'EntailmentTypeViewSet',
    'EventTypeViewSet',
    'InstitutionViewSet',
    'ItemViewSet',
    'ItemTypeViewSet',
    'LicenceViewSet',
    'LicenceTypeViewSet',
    'MetaCollectionViewSet',
    'PhysicalDeviceViewSet',
    'RoleViewSet',
    'SamplingEventViewSet',
    'SamplingEventTypeViewSet',
    'SchemaViewSet',
    'SecondaryItemViewSet',
    'SiteViewSet',
    'SiteTypeViewSet',
    'SourceViewSet',
    'SynonymViewSet',
    'SynonymSuggestionViewSet',
    'TagViewSet',
    'TermViewSet',
    'TermSuggestionViewSet',
    'TermTypeViewSet',
    'UserViewSet',
]
