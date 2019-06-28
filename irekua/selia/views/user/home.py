from django import forms

from selia.views.utils import SeliaDetailView
from database.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'institution'
        ]


class UserHomeView(SeliaDetailView):
    model = User
    form_class = UserUpdateForm
    template_name = 'selia/user/home.html'
    help_template = 'selia/components/help/user_home.html'
    detail_template = 'selia/components/details/user.html'
    summary_template = 'selia/components/summaries/user.html'
    update_form_template = 'selia/components/update/user.html'

    def get_object(self):
        return self.request.user

    def has_delete_permission(self):
        return False
