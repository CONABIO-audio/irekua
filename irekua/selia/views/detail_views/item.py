from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import Item
from selia.views.detail_views.base import SeliaDetailView
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


class DetailItemView(SeliaDetailView, SingleObjectMixin):
    model = Item
    form_class = CollectionItemUpdateForm
    delete_redirect_url = 'selia:collection_items'

    template_name = 'selia/detail/item.html'
    help_template = 'selia/components/help/collection_item_detail.html'
    detail_template = 'selia/components/details/item.html'
    summary_template = 'selia/components/summaries/item.html'
    update_form_template = 'selia/components/update/item.html'
    viewer_template = 'selia/components/viewers/item_image.html'

    def get_delete_redirect_url_args(self):
        return [self.object.collection.pk]

    def get_next_object(self):
        next_object = Item.objects.filter(pk__gt=self.kwargs['pk']).order_by('pk').first()
        return next_object

    def get_prev_object(self):
        prev_object = Item.objects.filter(pk__lt=self.kwargs['pk']).order_by('pk').last()
        return prev_object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection_device'] = self.object
        context["next_object"] = self.get_next_object()
        context["prev_object"] = self.get_prev_object()
        return context
