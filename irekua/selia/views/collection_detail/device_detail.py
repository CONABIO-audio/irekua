from django.views.generic import DetailView

from database.models import CollectionDevice


class CollectionDeviceDetailView(DetailView):
    model = CollectionDevice
    template_name = 'selia/collection_detail/device_detail.html'

    def get_context_data(self, *args, **kwargs):
        collection_device = self.object

        context = super().get_context_data(*args, **kwargs)
        context['collection'] = collection_device.collection
        return context
