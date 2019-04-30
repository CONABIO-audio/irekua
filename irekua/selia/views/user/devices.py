from selia.views.components.grid import GridView
from rest.filters.physical_devices import Filter
from django import forms


from database.models import PhysicalDevice


class PhysicalDeviceUpdateForm(forms.ModelForm):
    class Meta:
        model = PhysicalDevice
        fields = ['serial_number','metadata']

class UserDevices(GridView):
    template_name = 'selia/user/devices.html'
    table_view_name = 'rest-api:user-devices'
    filter_class = Filter
    update_form = PhysicalDeviceUpdateForm

    update_form_url = '/selia/widgets/update_form/PhysicalDevice/'

    include_map = False

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
