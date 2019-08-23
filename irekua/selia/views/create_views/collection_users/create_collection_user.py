from django import forms

from selia.views.utils import SeliaCreateView
from database.models import Collection
from database.models import CollectionUser
from database.models import Role
from database.models import User

from selia.forms.json_field import JsonField


class CreateCollectionUserForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionUser
        fields = [
            'collection',
            'user',
            'role',
            'metadata',
        ]


class CreateCollectionUserView(SeliaCreateView):
    template_name = 'selia/create/collection_users/create_form.html'
    success_url = 'selia:collection_users'

    model = CollectionUser
    form_class = CreateCollectionUserForm

    def get_initial(self, *args, **kwargs):
        self.collection = Collection.objects.get(
            name=self.request.GET['collection'])
        self.user = User.objects.get(
            name=self.request.GET['user'])
        self.role = Role.objects.get(
            name=self.request.GET['role'])

        return {
            'collection': self.collection,
            'role': self.role,
            'user': self.user,
        }

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['user'] = self.user
        context['role'] = self.role

        context['form'].fields['metadata'].update_schema(
            self.role.metadata_schema)
        return context
