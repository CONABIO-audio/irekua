from django import forms
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from database.models import CollectionSite
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

class CollectionSiteCreateForm(forms.ModelForm):
    class Meta:
        model = CollectionSite
        fields = [
            'site_type',
            'metadata',
            'site',
            'collection',
            'internal_id',
        ]

class CollectionSiteCreateView(CreateView, SingleObjectMixin):
    template_name = 'selia/collection_detail/sites/create.html'
    model = CollectionSite
    success_url = 'selia:collection_sites'
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

    def handle_site_created(self,site):
        query = self.request.GET.copy()
        query['site'] = site.pk
        query['selected_site'] = site.pk

        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'sites')
        return redirect(url)

    def handle_create(self):
        form = CollectionSiteCreateForm(self.request.POST)
        print(form.data)
        if form.is_valid():
            print("form is valid!!!")
            collection_site = CollectionSite()
            collection_site.site_type = form.cleaned_data.get('site_type')
            collection_site.metadata = form.cleaned_data.get('metadata')
            collection_site.site = form.cleaned_data.get('site')
            collection_site.collection = form.cleaned_data.get('collection')
            collection_site.internal_id = form.cleaned_data.get('internal_id')
            collection_site.created_by = self.request.user
            collection_site.save()


            return self.handle_finish_create()
        else:
            print("Not valid!")
            print(form.errors)
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def handle_create_site(self):
        form = SiteCreateForm(self.request.POST)
        print(form.data)
        if form.is_valid():
            print("form is valid!!!")
            site = Site()
            site.latitude = form.cleaned_data.get('latitude')
            site.longitude = form.cleaned_data.get('longitude')
            site.altitude = form.cleaned_data.get('altitude')
            site.name = form.cleaned_data.get('name')
            site.locality = form.cleaned_data.get('locality')
            site.created_by = self.request.user
            site.save()

            return self.handle_site_created(site)
        else:
            print("Not valid!")
            print(form.errors)
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            
            return self.render_to_response(context)
         

    def post(self, *args, **kwargs):
        fase = self.request.GET.get('fase', None)
        if fase == "create_site":
            return self.handle_create_site()
        else:        
            return self.handle_create()



    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'site' in self.request.GET:
            initial['site'] = Site.objects.get(pk=self.request.GET['site'])

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.get_object(queryset=Collection.objects.all())
        context['site_create_form'] = SiteCreateForm()
        context['site_list'] = self.get_site_list()

        if 'site' in self.request.GET:
            site = Site.objects.get(pk=self.request.GET['site'])
            context['selected_site'] = site
        if 'success_url' in self.request.GET:
            context["success_url"] = self.request.GET["success_url"]
        else:
            context["success_url"] = self.success_url

        return context
