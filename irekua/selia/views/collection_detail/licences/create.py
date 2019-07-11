from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from database.models import Collection
from database.models import Licence


class LicenceCreateView(CreateView, SingleObjectMixin):
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

    def get_site_list(self):
        return Licence.objects.exclude(collectionsite__collection=self.get_object(queryset=Collection.objects.all()))

    def get_success_url(self):
        if 'success_url' in self.request.GET:
            successurl = self.request.GET["success_url"]
        else:
            successurl = self.success_url

        return reverse(successurl, args=[self.kwargs['pk']])

    def handle_finish_create(self):
        return redirect(self.get_success_url())

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

        if 'success_url' in self.request.GET:
            context["success_url"] = self.request.GET["success_url"]
        else:
            context["success_url"] = self.success_url

        return context
