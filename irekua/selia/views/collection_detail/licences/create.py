from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaCreateView
from django.urls import reverse
from database.models import Collection
from database.models import Licence


class CollectionLicenceCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/licences/create.html'
    model = Licence
    success_url = 'selia:collection_licences'
    fields = [
        'licence_type',
        'document',
        'metadata',
        'collection',
    ]

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            licence = form.save(commit=False)
            licence.created_by = self.request.user
            licence.save()
            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.get_object(queryset=Collection.objects.all())
        return context
