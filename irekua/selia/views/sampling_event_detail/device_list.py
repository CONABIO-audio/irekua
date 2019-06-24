from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator

from database.models import SamplingEvent


class SamplingEventDevicesListView(SingleObjectMixin, ListView):
    template_name = 'selia/sampling_event_detail/device_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SamplingEvent.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        sampling_event = self.object
        queryset = sampling_event.samplingeventdevice_set.all()
        paginator = Paginator(queryset, 10)

        page = self.request.GET.get('page', 10)
        return paginator.get_page(page)

    def get_context_data(self, *args, **kwargs):
        sampling_event = self.object

        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = sampling_event
        return context
