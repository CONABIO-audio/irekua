from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import CollectionSite
from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionSiteUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionSite
        fields = [
            'internal_id',
            'metadata',
        ]


class DetailCollectionSiteView(SeliaDetailView, SingleObjectMixin):
    model = CollectionSite
    form_class = CollectionSiteUpdateForm
    delete_redirect_url = 'selia:collection_sites'

    template_name = 'selia/detail/collection_site.html'
    help_template = 'selia/components/help/collection_site_detail.html'
    detail_template = 'selia/components/details/collection_site.html'
    summary_template = 'selia/components/summaries/collection_site.html'
    update_form_template = 'selia/components/update/collection_site.html'
    viewer_template = 'selia/components/viewers/collection_site.html'

    def get_delete_redirect_url_args(self):
        return [self.object.collection.pk]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_site'] = self.object
        context['collection'] = self.object.collection

        schema = self.object.site_type.metadata_schema
        context['form'].fields['metadata'].update_schema(schema)
        return context