from .about import about
from .home import home
from .user.home import user_home

from .user.sites import UserSites
from .user.devices import UserDevices
from .user.items import UserItems
from .user.sampling_events import UserSamplingEvents
from .user.form_creator import UserFormCreator


from .sampling_events.home import SamplingEventHome
from .sampling_events.items import SamplingEventItems
from .sampling_events.devices import SamplingEventDevices

from .data_collections.data_collections import UserCollections
from .data_collections.open_collections import OpenCollections
from .data_collections.detail.home import collection_home
from .data_collections.detail.devices import CollectionDevices
from .data_collections.detail.items import CollectionItems
from .data_collections.detail.sampling_events import CollectionSamplingEvents
from .data_collections.detail.sites import CollectionSites

from .sampling_devices.home import SamplingEventDeviceHome
from .sampling_devices.items import SamplingEventDeviceItems
from .sampling_devices.item_detail import item

from .update_session import update_session

from .upload import upload
from .upload import photo_list
from .upload import upload_photo

from .test import TestView
