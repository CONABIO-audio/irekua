from django.utils.translation import gettext as _

from database.models import PhysicalDevice

from irekua_utils.filters.devices import physical_devices
from selia.views.utils import SeliaListView


class UserPhysicalDeviceListView(SeliaListView):
    template_name = 'selia/user/device_list.html'
    empty_message = _('User has no registered devices')
    filter_class = physical_devices.Filter
    search_fields = physical_devices.search_fields
    ordering_fields = physical_devices.ordering_fields

    def get_initial_queryset(self):
        return PhysicalDevice.objects.filter(created_by=self.request.user)
