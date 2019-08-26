from django import forms

from selia.views.utils import SeliaCreateView
from database.models import Collection
from database.models import Licence
from database.models import LicenceType

from selia.forms.json_field import JsonField


class CreateLicenceForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Licence
        fields = [
            'licence_type',
            'document',
            'metadata',
            'collection',
        ]


class CreateLicenceView(SeliaCreateView):
    template_name = 'selia/create/licences/create_form.html'
    success_url = 'selia:collection_licences'

    model = Licence
    form_class = CreateLicenceForm

    def get_initial(self, *args, **kwargs):
        self.collection = Collection.objects.get(
            name=self.request.GET['collection'])
        self.licence_type = LicenceType.objects.get(
            name=self.request.GET['licence_type'])
        return {
            'collection': self.collection,
            'licence_type': self.licence_type,
        }

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['licence_type'] = self.licence_type

        context['form'].fields['metadata'].update_schema(
            self.licence_type.metadata_schema)
        return context
