from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaCreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from database.models import Site


class UserSiteCreateView(SeliaCreateView):
    template_name = 'selia/user/sites/create.html'
    model = Site
    success_url = 'selia:user_sites'
    fields = [
            'latitude',
            'longitude',
            'altitude',
            'name',
            'locality',
            ]            

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            site = form.save(commit=False)
            site.created_by = self.request.user
            site.save()
            return self.handle_finish_create(site)
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)         


    def get_initial(self):
        initial = {
            'user': self.request.user
        }

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user'] = self.request.user

        return context
