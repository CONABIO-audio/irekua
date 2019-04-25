from django.views.generic.detail import DetailView

from selia.utils import ModelSerializer
from database.models import SamplingEvent


class SamplingEventSerializer(ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = '__all__'


class SamplingEventHome(DetailView):
    template_name = 'selia/sampling_events/home.html'
    model = SamplingEvent
    pk_url_kwarg = 'sampling_event_id'

    serializer_class = SamplingEventSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)

        context['serialized_object'] = self.serializer_class(self.get_object(), many=False)
        return context
