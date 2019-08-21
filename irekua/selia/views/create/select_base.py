from django.views.generic import TemplateView
from django.shortcuts import render


class SeliaSelectView(TemplateView):
    no_permission_template = 'selia/no_permission.html'
    prefix = ''

    def get_list_class(self):
        if hasattr(self, 'list_class'):
            return self.list_class

        msg = 'User did not supply a list class or overwrite get list class method'
        raise NotImplementedError(msg)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['{}_list'.format(self.prefix)] = self.get_list_context_data()
        return context

    def get_list_context_data(self):
        list_class = self.get_list_class()

        if not list_class.prefix:
            list_class.prefix = self.prefix

        list_instance = list_class()
        return list_instance.get_context_data(self.request)

    def has_view_permission(self):
        return True

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)
