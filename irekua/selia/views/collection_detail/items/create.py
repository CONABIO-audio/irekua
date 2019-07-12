from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import Collection
from database.models import Item

class CollectionItemCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/items/create.html'
    model = Item
    success_url = 'selia:collection_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_sampling_event_list(self):
        queryset = SamplingEvent.objects.filter()
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)

        return page

    def get_sampling_event_device_list(self):
        print(self.request.GET)
        if 'sampling_event' in self.request.GET:
            sampling_event = self.request.GET.get('sampling_event', None)
            queryset = SamplingEventDevice.objects.filter(sampling_event__pk=sampling_event)
            paginator = Paginator(queryset,5)
            page = self.request.GET.get('page',1)
            page = paginator.get_page(page)

            return page
        else:
            return EmptyPage()


    def get_success_url(self):
        return reverse('selia:collection_sampling_events', args=[self.kwargs['pk']])

    def handle_finish_create(self):
        next_url = self.request.GET.get('next', None)
        return redirect(next_url)

    def handle_create(self):
        form = self.get_form()
        print(form.data)
        if form.is_valid():
            Item = form.save(commit=False)
            Item.created_by = self.request.user
            Item.save()
            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def post(self, *args, **kwargs):
        return self.handle_create()

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'sampling_event' in self.request.GET:
            print(self.request.GET["sampling_event"])
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
