from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from database.models import Licence
from database.models import Collection
from database.models import Site


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'latitude',
            'longitude',
            'altitude',
            'name',
            'locality',
        ]

class LicenceCreateForm(forms.ModelForm):
    class Meta:
        model = Licence
        fields = [
            'site_type',
            'metadata',
            'site',
            'collection',
            'internal_id',
        ]

class LicenceCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/sites/create.html'
    model = Licence
    success_url = 'selia:licences'
    fields = [
            'site_type',
            'metadata',
            'site',
            'collection',
            'internal_id',
            ]

    def check_perms_or_redirect(self):
        return True

    def get(self, *args, **kwargs):
        self.check_perms_or_redirect()
        return super().get(*args, **kwargs)

    def get_site_list(self):
        return Site.objects.exclude(collectionsite__collection=self.get_object(queryset=Collection.objects.all()))

    def get_success_url(self):
        if 'success_url' in self.request.GET:
            successurl = self.request.GET["success_url"]
        else:
            successurl = self.success_url

        return reverse(successurl, args=[self.kwargs['pk']])

    def handle_finish_create(self):
        next_url = self.request.GET.get('next', None)
        return redirect(next_url)

    def handle_create(self):
        form = LicenceCreateForm(self.request.POST)
        print(form.data)
        if form.is_valid():
            print("form is valid!!!")
            licence = Licence()
            licence.licence_type = form.cleaned_data.get('licence_type')
            licence.metadata = form.cleaned_data.get('metadata')
            licence.document = form.cleaned_data.get('document')
            licence.collection = form.cleaned_data.get('collection')
            licence.created_by = self.request.user
            licence.save()

            return self.handle_finish_create()
        else:
            print("Not valid!")
            print(form.errors)
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
