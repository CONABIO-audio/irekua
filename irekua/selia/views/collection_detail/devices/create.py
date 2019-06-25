from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin

from database.models import CollectionDevice
from database.models import Collection


class CollectionDeviceCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/devices/create.html'
    model = CollectionDevice
    fields = ['physical_device', 'collection', 'internal_id', 'metadata']

    def get_device_list(self):
        user = self.request.user
        user_devices = user.physicaldevice_created_by.all()

        collection = self.get_object(queryset=Collection.objects.all())
        collection_user_devices = collection.physical_devices.filter(created_by=user)

        return user_devices.difference(collection_user_devices)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs) 
        context['collection'] = self.get_object(queryset=Collection.objects.all())
        context['device_list'] = self.get_device_list()
        return context
