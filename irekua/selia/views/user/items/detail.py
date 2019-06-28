from django import forms

from database.models import Item
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField


class ItemUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Item
        fields = [
            'metadata',
            'tags',
        ]


class UserItemDetailView(SeliaDetailView):
    model = Item
    form_class = ItemUpdateForm
    template_name = 'selia/user/items/detail.html'
    help_template = 'selia/components/help/item.html'
    detail_template = 'selia/components/details/item.html'
    summary_template = 'selia/components/summaries/item.html'
    update_form_template = 'selia/components/update/item.html'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)

        schema = self.object.item_type.metadata_schema
        form.fields['metadata'].update_schema(schema)
        return form
