from django import forms

from database.models import CollectionSite
from database.models import Collection
from database.models import Site
from database.models import SiteType

from selia.forms.json_field import JsonField
from selia.views.create_views.create_base import SeliaCreateView


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
    model = CollectionSite
    form_class = CollectionSiteCreateForm

    template_name = 'selia/create/collection_sites/create_form.html'
    success_url = 'selia:collection_sites'

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_initial(self):
        self.collection = Collection.objects.get(
            pk=self.request.GET['collection'])
        self.site = Site.objects.get(
            pk=self.request.GET['site'])
        self.site_type = SiteType.objects.get(
            pk=self.request.GET['site_type'])

        return {
            'collection': self.collection,
            'site': self.site,
            'site_type': self.site_type,
        }

    def get_additional_query_on_sucess(self):
        return {
            'collection': self.object.collection.pk,
            'collection_site': self.object.pk
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['site'] = self.site
        context['site_type'] = self.site_type

        context['form'].fields['metadata'].update_schema(
            self.site_type.metadata_schema)

        return context
