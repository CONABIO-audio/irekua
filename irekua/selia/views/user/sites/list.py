from django.utils.translation import gettext as _

from database.models import Site

from irekua_utils.filters import sites
from selia.views.utils import SeliaListView


class UserSitesListView(SeliaListView):
    template_name = 'selia/user/sites/list.html'
    list_item_template = 'selia/components/list_items/site.html'
    help_template = 'selia/components/help/user_sites.html'
    filter_form_template = 'selia/components/filters/sites.html'

    empty_message = _('User has no registered sites')
    filter_class = sites.Filter
    search_fields = sites.search_fields
    ordering_fields = sites.ordering_fields

    def get_initial_queryset(self):
        return Site.objects.filter(created_by=self.request.user)
