from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaCreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator
from database.models import SamplingEvent


class UserSamplingEventCreateView(SeliaCreateView):
    template_name = 'selia/user/sampling_events/create.html'
    model = SamplingEvent
    success_url = 'selia:user_sampling_events'
    fields = []


    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

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
        context['success_url'] =self.get_success_url()

        return context
