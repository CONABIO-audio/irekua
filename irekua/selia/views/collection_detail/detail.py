from django.views.generic import DetailView

from database.models import Collection


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'selia/collection_detail/detail.html'

    def get_context_data(self, *args, **kwargs):
        collection = self.object

        context = super().get_context_data(*args, **kwargs)
        context['collection'] = collection
        return context
