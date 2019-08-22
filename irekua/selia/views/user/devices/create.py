from django import forms
from django.shortcuts import redirect
from django.contrib.auth.models import Permission
from dal import autocomplete

from database.models import PhysicalDevice
from database.models import Device
from database.models import DeviceBrand
from database.models import DeviceType

from selia.views.utils import SeliaCreateView
from selia.forms.type_field import TypeSelectField


class SelectDeviceForm(forms.Form):
    device = forms.ModelChoiceField(
        required=False,
        queryset=Device.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='selia:devices_autocomplete',
            attrs={'style': 'width: 100%'}))
    device_type = TypeSelectField(
        required=False,
        queryset=DeviceType.objects.all())
    brand = forms.ModelChoiceField(
        required=False,
        queryset=DeviceBrand.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='selia:device_brands_autocomplete',
            attrs={'style': 'width: 100%'}))
    model = forms.CharField(required=False)


class CreateDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'device_type',
            'brand',
            'model'
        ]


class PhysicalDeviceCreateForm(forms.ModelForm):
    class Meta:
        model = PhysicalDevice
        fields = [
            'device',
            'metadata',
            'serial_number',
            'identifier',
            'bundle',
        ]


class UserPhysicialDeviceCreateView(SeliaCreateView):
    template_name = 'selia/user/devices/create.html'
    create_form_template = 'selia/components/create/user_physical_device.html'
    success_url = 'selia:user_devices'
    model = PhysicalDevice
    form_class = PhysicalDeviceCreateForm

    def get(self, *args, **kwargs):
        permission = Permission.objects.get(name='Can add Device Brand')
        self.request.user.user_permissions.add(permission)
        return super().get(*args, **kwargs)

    def get_initial(self):
        initial = {}

        if 'device' in self.request.GET:
            device_pk = self.request.GET['device']
            initial['device'] = Device.objects.get(pk=device_pk)

        return initial

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            physical_device = form.save(commit=False)
            physical_device.created_by = self.request.user
            physical_device.save()
            return self.handle_finish_create(physical_device)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def handle_select_device_fase(self):
        form = SelectDeviceForm(self.request.POST)
        if form.is_valid():
            device = form.cleaned_data['device']
            if device is not None:
                return self.handle_select_device(device)

            data = form.cleaned_data.copy()
            new_device_form = CreateDeviceForm(data)
            if new_device_form.is_valid():
                device = new_device_form.save()
                return self.handle_select_device(device)

        context = self.get_context_data()
        context['device_form'] = new_device_form
        return self.render_to_response(context)

    def handle_select_device(self, device):
        query = self.request.GET.copy()
        query['fase'] = 'add_details'
        query['device'] = device.pk
        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'addDetails')
        return redirect(url)

    def post(self, *args, **kwargs):
        fase = self.request.GET.get('fase', None)
        if fase == 'select_device':
            return self.handle_select_device_fase()

        return super().post(*args, **kwargs)

    def get_select_device_form(self):
        return SelectDeviceForm({})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['select_device_form'] = self.get_select_device_form()

        if 'device' in self.request.GET:
            device = Device.objects.get(pk=self.request.GET['device'])
            context['device'] = device

        return context
