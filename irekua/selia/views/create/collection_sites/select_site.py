from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse

from database.models import Collection
from database.models import Site

from irekua_utils.filters import sites as site_utils
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


class SelectCollectionSiteSiteView(SeliaCreateView):
    model = Site
    form_class = SiteCreateForm
    template_name = 'selia/create/collection_sites/select_site.html'

    def get_context_data(self):
        context = super().get_context_data()
        self.collection = Collection.objects.get(pk=self.request.GET['collection'])
        context['collection'] = self.collection
        context['site_list'] = self.get_site_list()
        return context

    def redirect_on_success(self):
        url = reverse('selia:create_collection_site')
        query = self.request.GET.copy()
        query['site'] = self.object.pk

        full_url = '{url}?{query}'.format(url=url, query=query.urlencode())
        return redirect(full_url)

    def get_fields_to_remove_on_sucess(self):
        return []

    def get_site_list(self):
        sites = (
            Site.objects
            .filter(created_by=self.request.user)
            .exclude(collectionsite__collection=self.collection)
        )

        class SiteList(SeliaList):
            prefix = 'sites'

            filter_class = site_utils.Filter
            search_fields = site_utils.search_fields
            ordering_fields = site_utils.ordering_fields

            queryset = sites

            list_item_template = 'selia/components/select_list_items/sites.html'
            filter_form_template = 'selia/components/filters/site.html'

        site_list = SiteList()
        return site_list.get_context_data(self.request)
