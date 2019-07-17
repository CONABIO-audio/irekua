from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from database.models import Collection
from database.models import Licence


class CollectionLicenceCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/licences/create.html'
    model = Licence
    success_url = 'selia:collection_licences'
    fields = [
            'licence_type',
            'document',
            'metadata',
            'collection',
            ]

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url, args=[self.kwargs['pk']])

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
            licence = form.save(commit=False)
            licence.created_by = self.request.user
            licence.save()
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

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.get_object(queryset=Collection.objects.all())

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        return context
