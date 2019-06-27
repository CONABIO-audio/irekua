from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from database.models import CollectionDevice
from database.models import Collection
from database.models import PhysicalDevice


class CollectionDeviceCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/devices/create.html'
    model = CollectionDevice
    fields = ['physical_device', 'collection', 'internal_id', 'metadata']

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_device_list(self):
        user = self.request.user
        user_devices = user.physicaldevice_created_by.all()

        collection = self.get_object(queryset=Collection.objects.all())
        collection_user_devices = collection.physical_devices.filter(created_by=user)

        return user_devices.difference(collection_user_devices)

    def get_success_url(self):
        return reverse('selia:collection_devices', args=[self.kwargs['pk']])

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'device' in self.request.GET:
            initial['physical_device'] = PhysicalDevice.objects.get(pk=self.request.GET['device'])

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.get_object(queryset=Collection.objects.all())
        context['device_list'] = self.get_device_list()

        if 'device' in self.request.GET:
            device = PhysicalDevice.objects.get(pk=self.request.GET['device'])
            context['selected_device'] = device

        return context
