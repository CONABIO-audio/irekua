from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import Item
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField


class CollectionItemUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Item
        fields = [
            'sampling_event_device',
            'captured_on',
            'tags',
            'metadata'
        ]


class CollectionItemDetailView(SeliaDetailView, SingleObjectMixin):
    model = Item
    form_class = CollectionItemUpdateForm

    template_name = 'selia/item_detail/detail.html'
    help_template = 'selia/components/help/collection_item_detail.html'
    detail_template = 'selia/components/details/item.html'
    summary_template = 'selia/components/summaries/item.html'
    update_form_template = 'selia/components/update/item.html'
    viewer_template = 'selia/components/viewers/item_image.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_device'] = self.object
        return context
