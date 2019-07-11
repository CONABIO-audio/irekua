from django import forms
from django.shortcuts import redirect
from django.contrib.auth.models import Permission
from dal import autocomplete

from database.models import CollectionSite
from database.models import Collection
from database.models import Site
from selia.views.utils import SeliaCreateView


class SelectSiteForm(forms.Form):
    site = forms.ModelChoiceField(
        required=False,
        queryset=Site.objects.filter(collectionsite__isnull=True))
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    altitude = forms.FloatField(required=False)
    name = forms.CharField(required=False)
    locality = forms.CharField(required=False)


class CreateSiteForm(forms.ModelForm):
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


class CollectionSiteCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/extra/create_site.html'
    create_form_template = 'selia/components/create/collection_site.html'
    success_url = 'selia:collection_sites'


    form_class = CollectionSiteCreateForm
    model = CollectionSite

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def handle_finish_details_fase(self):
        selected_site = self.request.GET.get('selected_site')
        prev_form = CollectionSiteCreateForm(self.request.POST)
        prev_data = prev_form.data.copy()
        prev_data["site"] = selected_site
        form = CollectionSiteCreateForm(prev_data)
        print(form.data)
        if form.is_valid():
            collection_site = CollectionSite()
            collection_site.site_type = form.cleaned_data.get('site_type')
            collection_site.metadata = form.cleaned_data.get('metadata')
            collection_site.site = form.cleaned_data.get('site')
            collection_site.collection = form.cleaned_data.get('collection')
            collection_site.internal_id = form.cleaned_data.get('internal_id')
            collection_site.created_by = self.request.user
            collection_site.save()

            return self.handle_finish_site(collection_site)
        else:
            print(form.errors)
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def handle_select_site_fase(self):
        form = SelectSiteForm(self.request.POST)
        if form.is_valid():
            site = form.cleaned_data['site']
            if  site is not None:
                return self.handle_select_site(site)

            data = form.cleaned_data.copy()
            new_site_form = CreateSiteForm(data)
            if new_site_form.is_valid():
                site = new_site_form.save()
                return self.handle_select_site(site)

            else:
                context = self.get_context_data()
                context['site_form'] = new_site_form
                self.object = None
                return self.render_to_response(context)
        else:
            print('No')

    def handle_finish_site(self,collection_site):
        next_url = self.request.GET.get('next', None)
        return redirect(next_url)

    def handle_select_site(self, site):
        query = self.request.GET.copy()
        query['fase'] = 'add_details'
        query['selected_site'] = site.pk

        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'addDetails')
        return redirect(url)

    def post(self, *args, **kwargs):
        fase = self.request.GET.get('fase', None)
        next_url = self.request.GET.get('next', None)
        if fase == 'select_site':
            return self.handle_select_site_fase()
        else:
            return self.handle_finish_details_fase()

    def get_select_site_form(self):
        data = {}

        if 'selected_site' in self.request.GET:
            return Site.objects.get(pk=self.request.GET['selected_site'])

        return SelectSiteForm(data)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['fase'] = self.request.GET.get('fase', 'select_site')
        context['select_site_form'] = self.get_select_site_form()
        context['collection'] = Collection.objects.get(pk=self.kwargs['pk'])
        return context
