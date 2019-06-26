from django.views.generic import DetailView

from database.models import CollectionSite


class CollectionSiteDetailView(DetailView):
    model = CollectionSite
    template_name = 'selia/collection_detail/sites/detail.html'

    def get_context_data(self, *args, **kwargs):
        collection_device = self.object

        context = super().get_context_data(*args, **kwargs)
        context['collection'] = collection_device.collection
        return context
