from django.http import HttpResponse
from django.views.generic import TemplateView


class GridView(TemplateView):
    template_name = "selia/test.html"

    def post(self, request, *args, **kwargs):
        print(request.POST)

    def get_filter_class(self):
        return self.filter_class

    def get_filter(self):
        filter_class = self.get_filter_class()
        queryset = self.get_queryset()
        filter_instance = filter_class(self.request.GET, queryset=queryset)
        return filter_instance

    def get_queryset(self):
        try:
            return self.queryset
        except AttributeError:
            return None

    def get_context_data(self):
        filter_instance = self.get_filter()
        return {'filter_form': filter_instance}
