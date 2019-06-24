from django.views.generic import ListView
from django.core.paginator import Paginator
from database.models import Collection


class OpenCollectionsView(ListView):
    template_name = 'selia/collections/open.html'
    context_object_name = 'collection_list'

    def get_queryset(self):
        queryset = Collection.objects.filter(is_open=True)
        paginator = Paginator(queryset, 10)

        page = self.request.GET.get('page', 10)
        return paginator.get_page(page)
