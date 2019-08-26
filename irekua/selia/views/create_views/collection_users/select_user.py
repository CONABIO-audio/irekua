from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from database.models import Collection
from database.models import User

from selia.views.utils.create_base import SeliaCreateView


class SelectUserForm(forms.Form):
    email = forms.EmailField(
        label=_('User email'))


class SelectCollectionUserUserView(SeliaCreateView):
    template_name = 'selia/create/collection_users/select_user.html'
    prefix = 'user'
    form_class = SelectUserForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs.pop('instance')
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = Collection.objects.get(
            name=self.request.GET['collection'])
        return context

    def save_form(self, form):
        try:
            return User.objects.get(
                email=form.cleaned_data['email'])
        except User.DoesNotExist:
            msg = _(
                'No user with this email was found'
            )
            raise forms.ValidationError({'email': msg})

    def redirect_on_success(self):
        url = reverse('selia:create_collection_user')
        query = self.request.GET.copy()
        query['user'] = self.object.pk

        full_url = '{url}?{query}'.format(url=url, query=query.urlencode())
        return redirect(full_url)
