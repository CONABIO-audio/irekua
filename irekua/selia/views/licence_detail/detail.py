from django.views.generic.detail import SingleObjectMixin
from django import forms

from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField
from database.models import Licence

class LicenceUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Licence
        fields = [
            'metadata',
            'document',
        ]

class LicenceDetailView(SeliaDetailView, SingleObjectMixin):
    model = Licence
    form_class = LicenceUpdateForm

    template_name = 'selia/licence_detail/detail.html'
    help_template = 'selia/components/help/collection_licences.html'
    detail_template = 'selia/components/details/licence.html'
    summary_template = 'selia/components/summaries/licence.html'
    update_form_template = 'selia/components/update/licence.html'
    viewer_template = 'selia/components/viewers/licence.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        licence = self.object
        context['licence'] = licence
        schema = licence.licence_type.metadata_schema
        context['form'].fields['metadata'].update_schema(schema)
        return context
