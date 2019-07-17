from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator
from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import CollectionDevice


class SamplingEventDeviceCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/sampling_event_detail/devices/create.html'
    model = SamplingEventDevice
    success_url = 'selia:sampling_event_devices'
    fields = [
            'sampling_event',
            'collection_device',
            'metadata',
            'commentaries',
            'configuration',
            'licence'
        ]

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_collection_device_list(self):
        queryset = CollectionDevice.objects.exclude(samplingeventdevice__sampling_event=self.get_object(queryset=SamplingEvent.objects.all()))
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
            return self.request.GET['back']+"?sampling_event="+self.kwargs['pk']+"&chain="+chain_str
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()

            return next_url+"?sampling_event="+self.kwargs['pk']+"&chain="+chain_str
            
    def handle_finish_create(self):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?sampling_event="+self.kwargs['pk']+"&chain="+chain_str
        
        return redirect(redirect_url)

    def get_success_url(self):
        return reverse(self.success_url, args=[self.kwargs['pk']])

    def handle_create(self):
        form = self.get_form()
        print(form.data)
        if form.is_valid():
            sampling_event_device = form.save(commit=False)
            sampling_event_device.created_by = self.request.user
            sampling_event_device.save()
            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.handle_create()



    def get_initial(self):
        sampling_event = SamplingEvent.objects.get(pk=self.kwargs['pk'])
        initial = {
            'sampling_event': sampling_event
        }

        if 'collection_device' in self.request.GET:
            initial['collection_device'] = CollectionDevice.objects.get(pk=self.request.GET['collection_device'])

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['sampling_event'] = self.get_object(queryset=SamplingEvent.objects.all())
        context['collection_device_list'] = self.get_collection_device_list()

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        if 'collection_device' in self.request.GET:
            collection_device = CollectionDevice.objects.get(pk=self.request.GET['collection_device'])
            context['selected_collection_device'] = collection_device

        return context
