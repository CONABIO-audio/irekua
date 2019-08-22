from django import forms

from database.models import Site
from selia.views.detail import SeliaDetailView


class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name',
            'locality',
            'latitude',
            'longitude',
            'altitude'
        ]


class DetailUserSiteView(SeliaDetailView):
    model = Site

    form_class = SiteUpdateForm

    template_name = 'selia/user/sites/detail.html'
    help_template = 'selia/components/help/user_sites.html'
    detail_template = 'selia/components/details/site.html'
    summary_template = 'selia/components/summaries/site.html'
    update_form_template = 'selia/components/update/site.html'
    viewer_template = 'selia/components/viewers/site.html'

    def has_view_permission(self):
        return self.object.created_by == self.request.user

    def has_delete_permission(self):
        return True

    def has_change_permission(self):
        return True
