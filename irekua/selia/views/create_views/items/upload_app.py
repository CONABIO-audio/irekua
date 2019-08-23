from django.views.generic import TemplateView
from django.shortcuts import render


class ItemUploadView(TemplateView):
    no_permission_template = 'selia/no_permission.html'
    template_name = 'selia/create/items/upload.html'

    def has_view_permission(self):
        return True

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)
