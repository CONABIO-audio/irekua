from django import forms

from database.models import Site
from selia.views.components.grid import GridView
from rest.filters.sites import UserFilter


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name',
            'locality',
            'latitude',
            'longitude',
            'altitude',
            'metadata'
        ]


class UserSites(GridView):
    template_name = 'selia/user/sites.html'
    table_view_name = 'rest-api:user-sites'
    map_view_name = 'rest-api:user-site-locations'
    filter_class = UserFilter
    update_form = UpdateForm

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}

    def get_map_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
