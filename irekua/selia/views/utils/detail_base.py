from django.views.generic import UpdateView
from django.shortcuts import render
from django.shortcuts import redirect


class SeliaDetailView(UpdateView):
    success_url = '#'
    no_permission_template = 'selia/no_permission.html'
    delete_redirect_url = 'selia:home'

    def get_update_form_template(self):
        if hasattr(self, 'update_form_template'):
            return self.update_form_template

        raise NotImplementedError('No template for update form was given')

    def get_detail_template(self):
        if hasattr(self, 'detail_template'):
            return self.detail_template

        raise NotImplementedError('No template for detail was given')

    def get_summary_template(self):
        if hasattr(self, 'summary_template'):
            return self.summary_template

        return ''

    def get_help_template(self):
        if hasattr(self, 'help_template'):
            return self.help_template

        raise NotImplementedError('No template for help was given')

    def has_view_permission(self):
        return True

    def has_change_permission(self):
        return True

    def has_delete_permission(self):
        return True

    def get_delete_redirect_url(self):
        if hasattr(self, 'delete_redirect_url'):
            return self.delete_redirect_url

        raise NotImplementedError('No redirect url was given in case of deletion')

    def get_permissions(self):
        permissions = {
            'change': self.has_change_permission(),
            'delete': self.has_delete_permission(),
        }
        return permissions

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def handle_delete(self):
        self.get_object().delete()
        redirect_to = self.get_delete_redirect_url()
        return redirect(redirect_to)

    def post(self, *args, **kwargs):
        if 'delete' in self.request.GET:
            return self.handle_delete()

        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.object = self.get_object()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['permissions'] = self.get_permissions()

        context['detail_template'] = self.get_detail_template()
        context['update_form_template'] = self.get_update_form_template()
        context['summary_template'] = self.get_summary_template()
        context['help_template'] = self.get_help_template()

        return context
