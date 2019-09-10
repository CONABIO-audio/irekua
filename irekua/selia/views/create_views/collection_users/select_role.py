from django.shortcuts import redirect
from django.urls import reverse

from database.models import Collection

from selia.views.create_views.select_base import SeliaSelectView


class SelectCollectionUserRoleView(SeliaSelectView):
    template_name = 'selia/create/collection_users/select_role.html'
    prefix = 'role'

    def should_redirect(self):
        self.collection = Collection.objects.get(pk=self.request.GET['collection'])

        collection_type = self.collection.collection_type
        self.role_types = collection_type.roles.all()

        return self.role_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_collection_user')

        query = self.request.GET.copy()
        query['role'] = self.role_types.first().pk
        full_url = '{url}?{query}'.format(
            url=url,
            query=query.urlencode())
        return redirect(full_url)

    def get_list_context_data(self):
        return self.role_types

    def get(self, *args, **kwargs):
        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        return context
