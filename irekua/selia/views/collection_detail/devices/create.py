from django import forms

from database.models import CollectionDevice
from database.models import Collection
from database.models import PhysicalDevice

from irekua_utils.filters.devices import physical_devices as device_utils

from selia.forms.json_field import JsonField
from selia.views.utils import SeliaCreateView
from selia.views.utils import SeliaList


class CollectionDeviceCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionDevice
        fields = [
            'physical_device',
            'collection',
            'internal_id',
            'metadata'
        ]


class CollectionDeviceCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/devices/create.html'
    model = CollectionDevice
    success_url = 'selia:collection_devices'
    form_class = CollectionDeviceCreateForm

    def handle_create(self):
        form = self.get_form()

        if form.is_valid():
            collection_device = form.save(commit=False)
            collection_device.created_by = self.request.user
            collection_device.save()
            return self.handle_finish_create(collection_device)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_device_list_context(self):
        user = self.request.user
        user_devices = user.physicaldevice_created_by.all()
        queryset_ = user_devices.exclude(collectiondevice__collection=self.collection)

        collection_type = self.collection.collection_type
        if collection_type.restrict_device_types:
            queryset_ = queryset_.filter(
                device__device_type__in=collection_type.device_types.all())

        class DeviceList(SeliaList):
            prefix = 'device_list'

            filter_class = device_utils.Filter
            search_fields = device_utils.search_fields
            ordering_fields = device_utils.ordering_fields

            queryset = queryset_

            list_item_template = 'selia/components/select_list_items/physical_devices.html'
            filter_form_template = 'selia/components/filters/physical_device.html'

        site_list = DeviceList()
        return site_list.get_context_data(self.request)

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        self.collection = self.get_object(queryset=Collection.objects.all())
        context['collection'] = self.collection
        context['device_list'] = self.get_device_list_context()

        if 'physical_device' in self.request.GET:
            device = PhysicalDevice.objects.get(pk=self.request.GET['physical_device'])
            context['physical_device'] = device
            schema = device.device.metadata_schema
            context['form'].fields['metadata'].update_schema(schema)

        return context
