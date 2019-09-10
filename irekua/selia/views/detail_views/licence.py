from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import Licence
from selia.views.detail_views.base import SeliaDetailView

from selia.forms.json_field import JsonField

class LicenceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Licence
        fields = [
            'metadata',
            'document',
        ]

class DetailLicenceView(SeliaDetailView, SingleObjectMixin):
    model = Licence
    form_class = LicenceUpdateForm
    delete_redirect_url = 'selia:collection_licences'

    template_name = 'selia/detail/licence.html'
    help_template = 'selia/components/help/collection_licences.html'
    detail_template = 'selia/components/details/licence.html'
    summary_template = 'selia/components/summaries/licence.html'
    update_form_template = 'selia/components/update/licence.html'
    viewer_template = 'selia/components/viewers/licence.html'

    def get_delete_redirect_url_args(self):
        return [self.object.collection.pk]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['licence'] = self.object
        context['collection'] = self.object.collection

        schema = self.object.licence_type.metadata_schema
        context['form'].fields['metadata'].update_schema(schema)
        return context
