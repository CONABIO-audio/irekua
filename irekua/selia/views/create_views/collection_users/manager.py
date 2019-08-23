from selia.views.create_views.manager_base import CreateManagerBase


class CreateCollectionUserManager(CreateManagerBase):
    required_get_parameters = ['collection']
    manager_name = 'selia:create_item'

    def view_from_request(self):
        if 'user' not in self.request.GET:
            return 'selia:create_collection_user_select_user'

        if 'role' not in self.request.GET:
            return 'selia:create_collection_user_select_role'

        return 'selia:create_collection_user_create_form'
