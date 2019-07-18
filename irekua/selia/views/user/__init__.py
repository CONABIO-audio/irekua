from .home import UserHomeView

from .items.list import UserItemsListView
from .sampling_events.list import UserSamplingEventsListView
from .sites.list import UserSitesListView
from .devices.list import UserPhysicalDeviceListView

from .items.detail import UserItemDetailView
from .items.create import UserItemCreateView

from .sampling_events.detail import UserSamplingEventDetailView
from .sampling_events.create import UserSamplingEventCreateView
from .sites.detail import UserSiteDetailView
from .sites.create import UserSiteCreateView

from .devices.detail import UserPhysicalDeviceDetailView
from .devices.create import UserPhysicialDeviceCreateView
