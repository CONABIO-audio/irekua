from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator
from database.models import SamplingEvent
from database.models import Collection
from database.models import Site
from database.models import CollectionSite


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

class SamplingEventCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/sampling_events/create.html'
    model = SamplingEvent
    success_url = 'selia:collection_sampling_events'
    fields = ['sampling_event_type','collection_site', 'collection','metadata','started_on','ended_on']

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_site_list(self):
        queryset = CollectionSite.objects.filter()
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
            return self.request.GET['back']+"?chain="+chain_str
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()

            return next_url+"?chain="+chain_str
            
    def handle_finish_create(self,new_object):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?&chain="+chain_str+"&created_object="+str(new_object.pk)
        
        return redirect(redirect_url)



    def handle_create(self):
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

            return self.handle_finish_create(sampling_event)
        else:
            print("Not valid!")
            print(form.errors)
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse(self.success_url, args=[self.kwargs['pk']])

    def post(self, *args, **kwargs):
        return self.handle_create()



    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'collection_site' in self.request.GET:
            initial['collection_site'] = CollectionSite.objects.get(pk=self.request.GET['collection_site'])

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.get_object(queryset=Collection.objects.all())
        context['site_list'] = self.get_site_list()

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        if 'collection_site' in self.request.GET:
            collection_site = CollectionSite.objects.get(pk=self.request.GET['collection_site'])
            context['selected_site'] = collection_site

        return context
