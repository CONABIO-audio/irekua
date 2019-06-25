from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator

from database.models import Collection
from database.models import Item


class CollectionItemsListView(SingleObjectMixin, ListView):
    template_name = 'selia/collection_detail/item_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Item.objects.filter(
            sampling_event_device__sampling_event__collection=self.object)
        paginator = Paginator(queryset, 10)

        page = self.request.GET.get('page', 1)
        return paginator.get_page(page)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object
        return context
