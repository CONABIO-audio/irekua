from django.views.generic import TemplateView


class AboutCollectionsView(TemplateView):
    template_name = 'selia/collections/about.html'
