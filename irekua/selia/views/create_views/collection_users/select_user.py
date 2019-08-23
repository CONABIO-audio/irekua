from database.models import Collection
from database.models import User

from selia.views.create_views.select_base import SeliaSelectView


class SelectCollectionUserUserView(SeliaSelectView):
    template_name = 'selia/create/collection_users/select_user.html'
    prefix = 'user'

    def get_list_context_data(self):
        return User.objects.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = Collection.objects.get(
            name=self.request.GET['collection'])
        return context
