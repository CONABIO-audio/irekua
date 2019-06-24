from django.views.generic import DetailView

from database.models import SamplingEvent


class SamplingEventDetailView(DetailView):
    model = SamplingEvent
    template_name = 'selia/sampling_event_detail/detail.html'

    def get_context_data(self, *args, **kwargs):
        sampling_event = self.object

        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = sampling_event
        return context
