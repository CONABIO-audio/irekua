from django import forms
from dal import autocomplete

from database.models import Collection
from selia.views.detail_views.base import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Collection
        fields = [
            'name',
            'institution',
            'description',
            'metadata',
            'logo'
        ]

        widgets = {
            'institution': autocomplete.ModelSelect2(url='selia:institutions_autocomplete')
        }


class DetailCollectionView(SeliaDetailView):
    model = Collection
    form_class = CollectionUpdateForm

    template_name = 'selia/detail/collection.html'

    help_template = 'selia/components/help/collection_detail.html'
    detail_template = 'selia/components/details/collection.html'
    summary_template = 'selia/components/summaries/collection.html'
    update_form_template = 'selia/components/update/collection.html'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        schema = self.object.collection_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
