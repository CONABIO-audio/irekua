from .about import about
from .home import home
from .user.home import user_home

from .user.sites import user_sites
from .user.devices import user_devices
from .user.items import user_items
from .user.sampling_events import user_sampling_events

from .sampling_events.home import sampling_event_home
from .sampling_events.items import sampling_event_items
from .sampling_events.devices import sampling_event_devices

from .data_collections.data_collections import user_collections
from .data_collections.open_collections import open_collections
from .data_collections.create_collection import create_collection
from .data_collections.detail.home import collection_home
from .data_collections.detail.devices import collection_devices
from .data_collections.detail.items import collection_items
from .data_collections.detail.sampling_events import collection_sampling_events
from .data_collections.detail.sites import collection_sites

from .sampling_devices.item_detail import item
from .sampling_devices.home import sampling_event_device

from .update_session import update_session

from .test import file_upload
