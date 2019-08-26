from django.shortcuts import redirect
from django.urls import reverse

from database.models import Collection
from database.models import LicenceType

from selia.views.create_views.select_base import SeliaSelectView


class SelectLicenceTypeView(SeliaSelectView):
    template_name = 'selia/create/licences/select_type.html'
    prefix = 'licence_type'

    def should_redirect(self):
        self.collection = Collection.objects.get(pk=self.request.GET['collection'])

        collection_type = self.collection.collection_type

        if collection_type.restrict_licence_types:
            self.licence_types = collection_type.licence_types.all()
        else:
            self.licence_types = LicenceType.objects.all()

        return self.licence_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_collection_site')

        query = self.request.GET.copy()
        query['licence_type'] = self.licence_types.first().pk
        full_url = '{url}?{query}'.format(
            url=url,
            query=query.urlencode())
        return redirect(full_url)

    def get_list_context_data(self):
        return self.licence_types

    def get(self, *args, **kwargs):
        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        return context
