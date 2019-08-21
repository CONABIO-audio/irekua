from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from database.models import Collection
from database.models import SamplingEventType


class SelectSamplingEventTypeView(TemplateView):
    template_name = 'selia/create/sampling_events/select_type.html'
    navbar_template = 'selia/collection_detail/components/secondary_navbar.html'

    def should_redirect(self):
        self.collection = Collection.objects.get(pk=self.request.GET['collection'])

        collection_type = self.collection.collection_type

        if collection_type.restrict_sampling_event_types:
            self.sampling_event_types = collection_type.sampling_event_types.all()
        else:
            self.sampling_event_types = SamplingEventType.objects.all()

        return self.sampling_event_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_sampling_event')
        full_url = '{url}?{query}&sampling_event_type={pk}'.format(
            url=url,
            query=self.request.GET.urlencode(),
            pk=self.sampling_event_types.first().pk)
        return redirect(full_url)

    def get(self, *args, **kwargs):
        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        context['sampling_event_types'] = self.sampling_event_types
        return context
