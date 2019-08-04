from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import gettext as _

from database.models import Annotation
from database.models import Item

from irekua_utils.filters.annotations import annotations
from selia.views.utils import SeliaListView



class CollectionAnnotationsListView(SeliaListView, SingleObjectMixin):
    paginate_by = 3
    template_name = 'selia/item_detail/annotations/list.html'
    list_item_template = 'selia/components/list_items/annotation.html'
    help_template = 'selia/components/help/item_annotations.html'
    filter_form_template = 'selia/components/filters/annotation.html'

    empty_message = _('There are no annotations for this item')

    filter_class = annotations.Filter
    search_fields = annotations.search_fields
    ordering_fields = annotations.ordering_fields

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Item.objects.all())
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return Annotation.objects.filter(item=self.object)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['item'] = self.object
        return context