from django.urls import reverse
from django.utils.html import mark_safe

from database.models import Item
from selia.views.annotations.base import SeliaAnnotationView


class CollectionItemAnnotatorView(SeliaAnnotationView):
    template_name = 'selia/annotations/annotator.html'

    def get_urls(self):
        return {
            'item': reverse('rest-api:item-detail', args=['item_pk']),
            'item_type': reverse('rest-api:itemtype-detail', args=[mark_safe('item_type_pk')])
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['pk'])
        context['urls'] = self.get_urls()
        return context
