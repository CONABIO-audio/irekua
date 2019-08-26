from selia.views.create_views.create_base import SeliaCreateView
from database.models import Site


class CreateSiteView(SeliaCreateView):
    template_name = 'selia/create/sites/create_form.html'
    success_url = 'selia:user_sites'

    model = Site
    fields = [
        'latitude',
        'longitude',
        'altitude',
        'name',
        'locality',
    ]

    def get_additional_query_on_sucess(self):
        return {
            'site': self.object.pk,
        }
