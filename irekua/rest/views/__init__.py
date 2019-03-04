from .annotation_types import AnnotationTypeViewSet
from .annotation_votes import AnnotationVoteViewSet
from .annotations import AnnotationViewSet
from .collection_devices import CollectionDeviceViewSet
from .collection_roles import CollectionRoleViewSet
from .collection_sites import CollectionSiteViewSet
from .collection_users import CollectionUserViewSet
from .data_collections import CollectionViewSet
from .device_brands import DeviceBrandViewSet
from .device_types import DeviceTypeViewSet
from .devices import DeviceViewSet
from .entailments import EntailmentViewSet
from .event_types import EventTypeViewSet
from .institutions import InstitutionViewSet
from .item_types import ItemTypeViewSet
from .items import ItemViewSet
from .licence_types import LicenceTypeViewSet
from .licences import LicenceViewSet
from .metacollections import MetaCollectionViewSet
from .physical_devices import PhysicalDeviceViewSet
from .role_types import RoleTypeViewSet
from .sampling_events import SamplingEventViewSet
from .schemas import SchemaViewSet
from .secondary_items import SecondaryItemViewSet
from .sites import SiteViewSet
from .sources import SourceViewSet
from .synonym_suggestions import SynonymSuggestionViewSet
from .synonyms import SynonymViewSet
from .term_suggestions import TermSuggestionViewSet
from .term_types import TermTypeViewSet
from .terms import TermViewSet
from .users import UserViewSet


__all__ = [
        'AnnotationTypeViewSet',
        'AnnotationViewSet',
        'AnnotationVoteViewSet',
        'CollectionDeviceViewSet',
        'CollectionRoleViewSet',
        'CollectionSiteViewSet',
        'CollectionUserViewSet',
        'CollectionViewSet',
        'DeviceBrandViewSet',
        'DeviceTypeViewSet',
        'DeviceViewSet',
        'EntailmentViewSet',
        'EventTypeViewSet',
        'InstitutionViewSet',
        'ItemTypeViewSet',
        'ItemViewSet',
        'LicenceTypeViewSet',
        'LicenceViewSet',
        'MetaCollectionViewSet',
        'PhysicalDeviceViewSet',
        'RoleTypeViewSet',
        'SamplingEventViewSet',
        'SchemaViewSet',
        'SecondaryItemViewSet',
        'SiteViewSet',
        'SourceViewSet',
        'SynonymSuggestionViewSet',
        'SynonymViewSet',
        'TermSuggestionViewSet',
        'TermTypeViewSet',
        'TermViewSet',
        'UserViewSet',
]
