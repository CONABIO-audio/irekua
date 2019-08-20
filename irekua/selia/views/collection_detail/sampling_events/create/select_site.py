from django.views.generic import TemplateView


class SelectSamplingEventSiteView(TemplateView):
    template_name = 'selia/collection_detail/sampling_events/create/select_site.html'
