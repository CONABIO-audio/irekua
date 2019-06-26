from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator

from database.models import Collection


class CollectionLicencesListView(SingleObjectMixin, ListView):
    template_name = 'selia/collection_detail/licence_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        collection = self.object
        queryset = collection.licence_set.all()
        paginator = Paginator(queryset, 10)

        page = self.request.GET.get('page', 1)
        return paginator.get_page(page)

    def get_context_data(self, *args, **kwargs):
        collection = self.object

        context = super().get_context_data(*args, **kwargs)
        context['collection'] = collection
        return context