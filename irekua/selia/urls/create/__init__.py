from . import sampling_events
from . import collection_sites
from . import items
from . import sampling_event_devices
from . import collection_devices
from . import physical_devices
from . import sites


urlpatterns = (
    sampling_events.urlpatterns +
    collection_sites.urlpatterns +
    items.urlpatterns +
    sampling_event_devices.urlpatterns +
    collection_devices.urlpatterns +
    physical_devices.urlpatterns +
    sites.urlpatterns
)
