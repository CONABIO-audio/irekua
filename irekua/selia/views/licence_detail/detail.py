from django.views.generic import DetailView

from database.models import Licence


class LicenceDetailView(DetailView):
    model = Licence
    template_name = 'selia/licence_detail/detail.html'

    def get_context_data(self, *args, **kwargs):
        licence = self.object

        context = super().get_context_data(*args, **kwargs)
        context['licence'] = licence
        return context