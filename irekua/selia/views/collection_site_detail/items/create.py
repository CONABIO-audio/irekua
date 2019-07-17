from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from database.models import SamplingEvent
from database.models import SamplingEventDevice
from database.models import CollectionSite
from database.models import Collection
from database.models import Item


class SamplingEventCreateForm(forms.ModelForm):
    class Meta:
        model = SamplingEvent
        fields = [
            'sampling_event_type',
            'collection_site',
            'metadata',
            'started_on',
            'ended_on',
            'collection'
        ]


class CollectionSiteItemCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_site_detail/items/create.html'
    model = Item
    success_url = 'selia:collection_site_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]


    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_sampling_event_list(self):
        queryset = SamplingEvent.objects.filter(collection_site=self.kwargs['pk'])
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
            back_url = self.request.GET['back']+"?"

            if 'sampling_event' in self.request.GET and 'sampling_event_device' in self.request.GET:
                back_url = back_url + "sampling_event="+self.request.GET["sampling_event"]+"&"

            return back_url+"chain="+chain_str
        elif 'sampling_event' in self.request.GET:
            return reverse('selia:collection_site_item_create', args=[self.kwargs['pk']])
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()

            return next_url+"?chain="+chain_str
            
    def handle_finish_create(self):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?chain="+chain_str
        
        return redirect(redirect_url)

    def get_success_url(self):
        return reverse(self.success_url, args=[self.kwargs['pk']])

    def handle_sampling_event_created(self,sampling_event):
        query = self.request.GET.copy()
        query['sampling_event'] = sampling_event.pk
        query['selected_sampling_event'] = sampling_event.pk

        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'sampling_events')
        return redirect(url)

    def handle_create(self):
        form = self.get_form()
        print(form.data)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = self.request.user
            item.save()
            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def handle_create_sampling_event(self):
        form = SamplingEventCreateForm(self.request.POST)
        print(form.data)
        if form.is_valid():
            print("form is valid!!!")
            sampling_event = SamplingEvent()
            sampling_event.collection_site = form.cleaned_data.get('collection_site')
            sampling_event.started_on = form.cleaned_data.get('started_on')
            sampling_event.ended_on = form.cleaned_data.get('ended_on')
            sampling_event.sampling_event_type = form.cleaned_data.get('sampling_event_type')
            sampling_event.metadata = form.cleaned_data.get('metadata')
            sampling_event.collection = form.cleaned_data.get('collection')
            sampling_event.created_by = self.request.user
            sampling_event.save()

            return self.handle_finish_create()
        else:
            print("Not valid!")
            print(form.errors)
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
         

    def post(self, *args, **kwargs):
        fase = self.request.GET.get('fase', None)
        if fase == "create_sampling_event":
            return self.handle_create_sampling_event()
        else:        
            return self.handle_create()



    def get_initial(self):
        initial = {
            'collection_site': CollectionSite.objects.get(pk=self.kwargs['pk'])
        }

        if 'sampling_event' in self.request.GET:
            initial['sampling_event'] = SamplingEvent.objects.get(pk=self.request.GET['sampling_event'])

        if 'sampling_event_device' in self.request.GET:
            initial['sampling_event_device'] = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])           

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection_site'] = self.get_object(queryset=CollectionSite.objects.all())
        context['sampling_event_create_form'] = SamplingEventCreateForm()
        context['sampling_event_list'] = self.get_sampling_event_list()
        context['sampling_event_device_list'] = self.get_sampling_event_device_list()

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        if 'sampling_event' in self.request.GET:
            sampling_event = SamplingEvent.objects.get(pk=self.request.GET['sampling_event'])
            context['selected_sampling_event'] = sampling_event


        if 'sampling_event_device' in self.request.GET:
            sampling_event_device = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])
            context['selected_sampling_event_device'] = sampling_event_device


        return context
