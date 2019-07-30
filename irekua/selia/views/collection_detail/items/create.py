from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaMultipleItemsCreateView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import Collection
from database.models import Item


class CollectionItemCreateView(SeliaMultipleItemsCreateView):
    template_name = 'selia/collection_detail/items/create.html'
    model = Item
    success_url = 'selia:collection_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]   

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def get_sampling_event_list(self):
        queryset = SamplingEvent.objects.filter()
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)

        return page

    def get_sampling_event_device_list(self):
        if 'sampling_event' in self.request.GET:
            sampling_event = self.request.GET.get('sampling_event', None)
            queryset = SamplingEventDevice.objects.filter(sampling_event__pk=sampling_event)
            paginator = Paginator(queryset,5)
            page = self.request.GET.get('page',1)
            page = paginator.get_page(page)

            return page
        else:
            return EmptyPage()


    def get_back_url(self):
        if 'back' in self.request.GET:
            chain_str = self.get_chain()
            back_url = self.request.GET['back']+"?"

            if 'sampling_event' in self.request.GET and 'sampling_event_device' in self.request.GET:
                back_url = back_url + "sampling_event="+self.request.GET["sampling_event"]+"&"

            return back_url+"chain="+chain_str
        elif 'sampling_event' in self.request.GET:
            return reverse('selia:collection_item_create', args=[self.kwargs['pk']])
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()

            return next_url+"?chain="+chain_str

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'sampling_event' in self.request.GET:
            initial['sampling_event'] = SamplingEvent.objects.get(pk=self.request.GET['sampling_event'])
        if 'sampling_event_device' in self.request.GET:
            initial['sampling_event_device'] = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])           

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.get_object(queryset=Collection.objects.all())
        context['sampling_event_list'] = self.get_sampling_event_list()
        context['sampling_event_device_list'] = self.get_sampling_event_device_list()

        if 'sampling_event' in self.request.GET:
            sampling_event = SamplingEvent.objects.get(pk=self.request.GET['sampling_event'])
            context['selected_sampling_event'] = sampling_event

        if 'sampling_event_device' in self.request.GET:
            sampling_event_device = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])
            context['selected_sampling_event_device'] = sampling_event_device


        return context
