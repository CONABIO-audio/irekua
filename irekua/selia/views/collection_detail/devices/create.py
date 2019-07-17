from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
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

        queryset =  user_devices.difference(collection_user_devices)
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)

        return page


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

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            collection_device = form.save(commit=False)
            collection_device.created_by = self.request.user
            collection_device.save()
            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.handle_create()

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

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        if 'device' in self.request.GET:
            device = PhysicalDevice.objects.get(pk=self.request.GET['device'])
            context['selected_device'] = device

        return context
