from . import sampling_events
from . import collection_sites
from . import items
from . import sampling_event_devices


urlpatterns = (
    sampling_events.urlpatterns +
    collection_sites.urlpatterns +
    items.urlpatterns +
    sampling_event_devices.urlpatterns
)
