from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator
from database.models import SamplingEvent


class UserSamplingEventCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/user/sampling_events/create.html'
    model = SamplingEvent
    success_url = 'selia:user_sampling_events'
    fields = []

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()

        if 'created_object' in self.request.GET:
            return self.handle_finish_create()
        else:
            return super().get(*args, **kwargs)

    def get_collection_list(self):
        queryset = self.request.user.collection_users.all()
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
            
    def handle_finish_create(self):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?&chain="+chain_str
        
        return redirect(redirect_url)


    def get_success_url(self):
        return reverse(self.success_url)

    def post(self, *args, **kwargs):
        return self.handle_create()

    def get_initial(self):
        initial = {
            'user': self.request.user,
            'success_url': self.get_success_url()
        }

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['user'] = self.request.user
        context['collection_list'] = self.get_collection_list()

        context['chain'] = self.get_chain()
        context['back'] = self.get_back_url()

        context['success_url'] =self.get_success_url()

        return context
