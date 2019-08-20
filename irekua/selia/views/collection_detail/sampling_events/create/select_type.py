from django.views.generic import TemplateView


class SelectSamplingEventTypeView(TemplateView):
    template_name = 'selia/collection_detail/sampling_events/create/select_type.html'
