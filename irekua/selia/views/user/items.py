from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Item
from selia.utils import ModelTable


class ItemTable(ModelTable):
    class Meta:
        model = Item
        fields = ['id', 'item_type', 'captured_on', 'licence']


@login_required(login_url='registration:login')
def user_items(request):
    user = request.user
    items = user.item_created_by.all()

    table = ItemTable(items, many=True)
    context = {'table': table}
    return render(request, 'selia/user/items.html', context)
