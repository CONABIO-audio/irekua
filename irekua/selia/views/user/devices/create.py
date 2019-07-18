from django import forms
from django.shortcuts import redirect
from django.contrib.auth.models import Permission
from dal import autocomplete

from database.models import PhysicalDevice
from database.models import Collection
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

    form_class = PhysicalDeviceCreateForm
    model = PhysicalDevice


    def get(self, *args, **kwargs):
        permission = Permission.objects.get(name='Can add Device Brand')
        self.request.user.user_permissions.add(permission)
        return super().get(*args, **kwargs)


    def get_chain(self):
        if 'chain' in self.request.GET:
            return self.request.GET.get('chain', None)
        else:
            return ''

    def get_new_chain(self):
        chain = self.get_chain()
        if chain != "":
            chain_arr = chain.split('|')
        else:
            chain_arr = []

        chain_str = ''
        next_url = ''
        if len(chain_arr) != 0:
            next_url = chain_arr[-1]
            chain_arr.pop(-1)
            if len(chain_arr) != 0:
                chain_str = "|".join(chain_arr)

        return chain_str, next_url

    def get_back_url(self):
        if 'back' in self.request.GET:
            chain_str = self.get_chain()
            return self.request.GET['back']+"?&chain="+chain_str
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()
                
            return next_url+"?&chain="+chain_str
            
    def handle_finish_create(self):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?&chain="+chain_str
        
        return redirect(redirect_url)

    def handle_finish_details_fase(self):
        selected_device = self.request.GET.get('selected_device')
        print("selected device")
        print(selected_device)
        prev_form = PhysicalDeviceCreateForm(self.request.POST)
        prev_data = prev_form.data.copy()
        prev_data["device"] = selected_device
        form = PhysicalDeviceCreateForm(prev_data)

        if form.is_valid():
            physical_device = PhysicalDevice()
            physical_device.identifier = form.cleaned_data.get('identifier')
            physical_device.serial_number = form.cleaned_data.get('serial_number')
            physical_device.device = form.cleaned_data.get('device')
            physical_device.metadata = form.cleaned_data.get('metadata')
            physical_device.bundle = form.cleaned_data.get('bundle')
            physical_device.created_by = self.request.user
            physical_device.save()

            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)



    def handle_select_device_fase(self):
        form = SelectDeviceForm(self.request.POST)
        if form.is_valid():
            device = form.cleaned_data['device']
            if  device is not None:
                return self.handle_select_device(device)

            data = form.cleaned_data.copy()
            new_device_form = CreateDeviceForm(data)
            if new_device_form.is_valid():
                device = new_device_form.save()
                return self.handle_select_device(device)

            else:
                context = self.get_context_data()
                context['device_form'] = new_device_form
                return self.render_to_response(context)
        else:
            print('No')

    def handle_select_device(self, device):
        query = self.request.GET.copy()
        query['fase'] = 'add_details'
        query['selected_device'] = device.pk

        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'addDetails')
        return redirect(url)

    def post(self, *args, **kwargs):
        fase = self.request.GET.get('fase', None)
        next_url = self.request.GET.get('next', None)
        if fase == 'select_device':
            return self.handle_select_device_fase()
        else:
            return self.handle_finish_details_fase()

    def get_select_device_form(self):
        data = {}

        if 'selected_device' in self.request.GET:
            return Device.objects.get(pk=self.request.GET['selected_device'])

        return SelectDeviceForm(data)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['fase'] = self.request.GET.get('fase', 'select_device')
        context['select_device_form'] = self.get_select_device_form()

        if 'selected_device' in self.request.GET:
            device = Device.objects.get(pk=self.request.GET['selected_device'])
            context['selected_device'] = device

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()
        
        return context
