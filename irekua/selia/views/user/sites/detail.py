from django import forms

from database.models import Site
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField


class SiteUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Site
        fields = [
            'name',
            'locality',
            'latitude',
            'longitude',
            'altitude'
        ]


class UserSiteDetailView(SeliaDetailView):
    model = Site
    form_class = SiteUpdateForm
    template_name = 'selia/user/sites/detail.html'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)

        schema = self.object.collection_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form
