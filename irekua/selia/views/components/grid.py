from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
import json
from django.urls import reverse
from django.views.generic import TemplateView


class GridView(TemplateView):
    template_name = "selia/test.html"
    with_table_links = False

    include_table = True
    include_map = True
    include_detail = True
    include_summary = True

    def enter_child(self, data):
        args = list(self.args) + [data['pk']]
        content = json.dumps({'url': reverse(self.child_view_name, args=args)})
        return HttpResponse(content, content_type='application/json')

    def get_handler(self, action):
        if action == 'enter':
            return self.enter_child

    def post(self, request):
        action = request.POST.get('action', None)
        if action is not None:
            handler = self.get_handler(action)
            return handler(request.POST)

        return super().get(request)

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

    def get_table_url_kwrags(self):
        raise NotImplementedError

    def get_table_url(self):
        kwargs = self.get_table_url_kwrags()
        return reverse(self.table_view_name, kwargs=kwargs)

    def get_table_context_data(self):
        filter_instance = self.get_filter()
        table_url = self.get_table_url()
        return {
            'table_url': table_url,
            'filter_form': filter_instance,
            'with_table_links': self.with_table_links
        }

    def get_grid_context_data(self):
        context = {
            'include_map': self.include_map,
            'include_detail': self.include_detail,
            'include_table': self.include_table,
            'include_summary': self.include_summary,
        }
        return context

    def get_context_data(self):
        context = {}
        context['grid_config'] = self.get_grid_context_data()
        context['table_info'] = self.get_table_context_data()
        return context
