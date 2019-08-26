from database.models import Licence
from database.models import SamplingEventDevice

from selia.views.create_views import SeliaSelectView


class SelectItemLicenceView(SeliaSelectView):
    template_name = 'selia/create/items/select_licence.html'
    prefix = 'licence'
    create_url = 'selia:create_item'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['sampling_event_device'] = SamplingEventDevice.objects.get(
            pk=self.request.GET['sampling_event_device'])
        return context

    def get_list_context_data(self):
        collection_pk = self.request.GET['collection']
        return Licence.objects.filter(collection__name=collection_pk)
