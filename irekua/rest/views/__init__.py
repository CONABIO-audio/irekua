from .annotation_tools import AnnotationToolViewSet
from .annotation_types import AnnotationTypeViewSet
from .collection_types import CollectionTypeViewSet
from .device_brands import DeviceBrandViewSet
from .device_types import DeviceTypeViewSet
from .devices import DeviceViewSet
from .entailment_types import EntailmentTypeViewSet
from .entailments import EntailmentViewSet
from .event_types import EventTypeViewSet
from .institutions import InstitutionViewSet
from .item_types import ItemTypeViewSet
from .items import (
    ItemViewSet,
    CollectionItemViewSet)
from .licence_types import LicenceTypeViewSet
from .licences import LicenceViewSet
from .metacollections import MetaCollectionViewSet
from .physical_devices import PhysicalDeviceViewSet
from .roles import RoleViewSet
from .sampling_event_types import SamplingEventTypeViewSet
from .sampling_events import (
    SamplingEventViewSet,
    CollectionSamplingEventViewSet)
from .site_types import SiteTypeViewSet
from .sites import SiteViewSet
from .synonym_suggestions import SynonymSuggestionViewSet
from .synonyms import SynonymViewSet
from .tags import TagViewSet
from .term_suggestions import TermSuggestionViewSet
from .term_types import TermTypeViewSet
from .terms import TermViewSet
from .users import UserViewSet
from .data_collections import CollectionViewSet


__all__ = [
    'AnnotationToolViewSet',
    'AnnotationTypeViewSet',
    'CollectionTypeViewSet',
    'CollectionItemViewSet',
    'CollectionSamplingEventViewSet',
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
]
