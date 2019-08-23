from selia.views.create_views.manager_base import CreateManagerBase


class CreateCollectionSiteManager(CreateManagerBase):
    required_get_parameters = ['collection']
    manager_name = 'selia:create_collection_site'

    def view_from_request(self):
        if 'site_type' not in self.request.GET:
            return 'selia:create_collection_site_select_type'

        if 'site' not in self.request.GET:
            return 'selia:create_collection_site_select_site'

        return 'selia:create_collection_site_create_form'
