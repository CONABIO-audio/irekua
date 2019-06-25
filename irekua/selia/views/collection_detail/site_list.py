from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator

from database.models import Collection


class CollectionSitesListView(SingleObjectMixin, ListView):
    template_name = 'selia/collection_detail/site_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.object.collectionsite_set.all()
        paginator = Paginator(queryset, 10)

        page = self.request.GET.get('page', 1)
        return paginator.get_page(page)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object

        show = self.request.GET.get('show', 'list')
        show_map = show == 'map'
        context['show_map'] = show_map

        if show_map:
            context['sites_map'] = 'bla'

        return context
