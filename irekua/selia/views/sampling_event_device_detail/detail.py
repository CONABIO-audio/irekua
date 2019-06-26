from django.views.generic import DetailView

from database.models import SamplingEventDevice


class SamplingEventDeviceDetailView(DetailView):
    model = SamplingEventDevice
    template_name = 'selia/sampling_event_device_detail/detail.html'

    def get_context_data(self, *args, **kwargs):
        sampling_event_device = self.object

        context = super().get_context_data(*args, **kwargs)
        context['sampling_event_device'] = sampling_event_device
        return context

