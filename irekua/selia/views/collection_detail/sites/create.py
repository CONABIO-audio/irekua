from django import forms
from django.shortcuts import redirect

from database.models import CollectionSite
from database.models import Collection
from database.models import Site
from database.models import SiteType

from irekua_utils.filters import sites as site_utils

from selia.forms.json_field import JsonField
from selia.views.utils import SeliaCreateView
from selia.views.utils import SeliaList


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
    metadata = JsonField()

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
    template_name = 'selia/collection_detail/sites/create.html'
    model = CollectionSite
    success_url = 'selia:collection_sites'
    form_class = CollectionSiteCreateForm

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def handle_site_created(self, site):
        query = self.request.GET.copy()
        query['site'] = site.pk
        query['selected_site'] = site.pk

        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'sites')
        return redirect(url)

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'site' in self.request.GET:
            site_pk = self.request.GET['site']
            initial['site'] = Site.objects.get(pk=site_pk)

        if 'site_type' in self.request.GET:
            initial['site_type'] = SiteType.objects.get(
                pk=self.request.GET['site_type'])

        return initial

    def handle_create(self):
        form = CollectionSiteCreateForm(self.request.POST)
        if form.is_valid():
            collection_site = form.save(commit=False)
            collection_site.created_by = self.request.user
            collection_site.save()
            return self.handle_finish_create(collection_site)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def handle_create_site(self):
        form = SiteCreateForm(self.request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.created_by = self.request.user
            site.save()
            return self.handle_site_created(site)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        fase = self.request.GET.get('fase', None)

        if fase == "create_site":
            return self.handle_create_site()

        return super().post(*args, **kwargs)

    def get_site_list_context(self):
        class SiteList(SeliaList):
            prefix = 'sites'

            filter_class = site_utils.Filter
            search_fields = site_utils.search_fields
            ordering_fields = site_utils.ordering_fields

            queryset = self.request.user.site_created_by.exclude(
                collectionsite__collection=self.collection)

            list_item_template = 'selia/components/select_list_items/sites.html'
            filter_form_template = 'selia/components/filters/site.html'

        site_list = SiteList()
        return site_list.get_context_data(self.request)

    def get_site_types(self):
        collection_type = self.collection.collection_type

        if collection_type.restrict_site_types:
            return collection_type.site_types.all()

        return SiteType.objects.all()

    def get_site_type(self, context):
        site_types = context['site_types']
        if site_types.count() == 1:
            return site_types.first()

        if 'site_type' in self.request.GET:
            site_type = SiteType.objects.get(
                pk=self.request.GET['site_type'])
            return site_type

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        self.collection = self.get_object(queryset=Collection.objects.all())

        context['collection'] = self.collection
        context['site_create_form'] = SiteCreateForm()
        context['site_list'] = self.get_site_list_context()
        context['site_types'] = self.get_site_types()

        if 'site' in self.request.GET:
            site = Site.objects.get(pk=self.request.GET['site'])
            context['site'] = site

        site_type = self.get_site_type(context)
        context['site_type'] = site_type

        if site_type:
            context['form'].fields['metadata'].update_schema(
                site_type.metadata_schema)

        return context
