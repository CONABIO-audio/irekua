from django.views.generic import CreateView
from django.shortcuts import render
from django.shortcuts import reverse


class SeliaCreateView(CreateView):
    no_permission_template = 'selia/no_permission.html'
    success_url = 'selia:home'

    def get_create_form_template(self):
        if hasattr(self, 'create_form_template'):
            return self.create_form_template

        raise NotImplementedError('No template for update form was given')

    def has_view_permission(self):
        return True

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get_success_url_args(self):
        return []

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']

        return reverse(self.success_url, args=self.get_success_url_args())

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['success_url'] = self.get_success_url()
        context['create_form_template'] = self.get_create_form_template()

        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']

        return context
