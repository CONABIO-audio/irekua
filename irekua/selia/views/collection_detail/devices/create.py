from selia.views.utils import SeliaCreateView
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
from database.models import CollectionDevice
from database.models import Collection
from database.models import PhysicalDevice


class CollectionDeviceCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/devices/create.html'
    model = CollectionDevice
    success_url = 'selia:collection_devices'
    fields = ['physical_device', 'collection', 'internal_id', 'metadata']

    def get_device_list(self):
        user = self.request.user
        user_devices = user.physicaldevice_created_by.all()

        collection = self.get_object(queryset=Collection.objects.all())
        collection_user_devices = collection.physical_devices.filter(created_by=user)

        queryset =  user_devices.difference(collection_user_devices)
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)

        return page

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            collection_device = form.save(commit=False)
            collection_device.created_by = self.request.user
            collection_device.save()
            return self.handle_finish_create(collection_device)
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def get_success_url(self):
        return reverse(self.success_url, args=[self.kwargs['pk']])

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
