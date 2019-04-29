from selia.views.components.grid import GridView
from rest.filters.items import Filter
from django import forms

from database.models import Item

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['metadata']

class UserItems(GridView):
    template_name = 'selia/user/items.html'
    table_view_name = 'rest-api:user-items'
    map_view_name = 'rest-api:user-item-locations'
    update_form = ItemUpdateForm
    filter_class = Filter

    def get_table_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}

    def get_map_url_kwargs(self):
        user = self.request.user
        return {"pk": user.pk}
