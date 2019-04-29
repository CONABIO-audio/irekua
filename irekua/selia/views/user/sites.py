from selia.views.components.grid import GridView
from rest.filters.sites import UserFilter
from django import forms

from database.models import Site


class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name','locality','site_type','altitude','metadata']

class UserSites(GridView):
    template_name = 'selia/user/grid.html'
    table_view_name = 'rest-api:user-sites'
    map_view_name = 'rest-api:user-site-locations'
    update_form = SiteUpdateForm
    filter_class = UserFilter

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}

    def get_map_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
