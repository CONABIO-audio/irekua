from .detail import CollectionDetailView

from .sampling_events.list import CollectionSamplingEventListView
from .sampling_events.create import SamplingEventCreateView

from .items.list import CollectionItemsListView
from .items.create import CollectionItemCreateView

from .devices.list import CollectionDevicesListView
from .devices.create import CollectionDeviceCreateView

from .sites.list import CollectionSitesListView
from .sites.create import CollectionSiteCreateView

from .licences.list import CollectionLicencesListView
from .licences.create import CollectionLicenceCreateView

from .users.list import CollectionUserListView
from .users.create import CollectionUserCreateView

from .extra.create_device import PhysicalDeviceCreateView

from .users.detail import CollectionUserDetailView
