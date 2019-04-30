from django import forms

from database.models import Item
from selia.views.components.grid import GridView
from rest.filters.items import Filter


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_file',
            'metadata',
            'captured_on',
        ]


class CollectionItems(GridView):
    template_name = 'selia/collections/detail/items.html'
    table_view_name = 'rest-api:collection-items'
    map_view_name = 'rest-api:collection-item-locations'
    filter_class = Filter
    update_form = UpdateForm

    update_form_url = '/selia/widgets/update_form/Item/'

    def get_table_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        return context
