from django.http import HttpResponse
from django.views.decorators.http import require_GET
from sorl.thumbnail import get_thumbnail
from irekua_utils.permissions.items import items as permissions
from database.models import Item
from django.shortcuts import redirect


@require_GET
def generate_thumbnail(request):
    item = Item.objects.get(pk=request.GET["pk"])
    im = get_thumbnail(item.item_thumbnail, '100x100', crop='center', quality=99)
    return redirect(im.url)


def no_permission_redirect():
    return None
