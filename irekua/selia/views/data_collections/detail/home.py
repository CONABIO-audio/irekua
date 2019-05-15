from django import forms

from database.models import Collection
from selia.views.components.grid import GridView


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'metadata',
            'description',
            'logo',
            'institution',
        ]


class CollectionHome(GridView):
    template_name = 'selia/collections/detail/home.html'
    detail_view_name = 'rest-api:collection-detail'
    update_form_url = '/selia/widgets/update_form/Collection/'
    update_form = UpdateForm
    detail = True

    include_map = False
    include_table = False
    # include_summary = True

    def get_detail_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        return context
