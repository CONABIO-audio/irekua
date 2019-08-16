from django import forms
from django.shortcuts import redirect

from database.models import CollectionUser
from database.models import Collection
from database.models import Role

from selia.forms.json_field import JsonField
from selia.views.utils import SeliaCreateView


class CollectionUserCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionUser
        fields = [
            'user',
            'collection',
            'role',
            'metadata',
        ]


class CollectionUserCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/users/create.html'
    success_url = 'selia:collection_users'
    form_class = CollectionUserCreateForm

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def handle_site_created(self, site):
        query = self.request.GET.copy()
        query['site'] = site.pk
        query['selected_site'] = site.pk

        url = '{}?{}#{}'.format(self.request.path, query.urlencode(), 'sites')
        return redirect(url)

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'role' in self.request.GET:
            site_pk = self.request.GET['role']
            initial['role'] = Role.objects.get(pk=site_pk)

        return initial

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            collection_site = form.save(commit=False)
            collection_site.created_by = self.request.user
            collection_site.save()
            return self.handle_finish_create(collection_site)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_roles(self):
        collection_type = self.collection.collection_type
        return collection_type.roles.all()

    def get_role(self, context):
        roles = context['roles']
        if roles.count() == 1:
            return roles.first()

        if 'role' in self.request.GET:
            role = Role.objects.get(
                pk=self.request.GET['role'])
            return role

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        self.collection = self.get_object(queryset=Collection.objects.all())

        context['collection'] = self.collection
        context['roles'] = self.get_roles()

        role = self.get_role(context)
        context['role'] = role

        if role:
            context['form'].fields['metadata'].update_schema(
                role.metadata_schema)

        return context
