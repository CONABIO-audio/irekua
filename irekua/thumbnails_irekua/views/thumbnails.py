from django.http import HttpResponse
from django.views.decorators.http import require_GET
from sorl.thumbnail import get_thumbnail
from irekua_utils.permissions.items import items as permissions
from database.models import Item
from django.shortcuts import redirect


@require_GET
def generate_thumbnail(request):
    #if not permissions.view_thumbnail(request.user):
    #    return no_permission_redirect()

    item = Item.objects.get(pk=request.GET["pk"])
    size = '100x100'
    crop = 'center'
    quality = 99

    if 'size' in request.GET:
    	size = request.GET["size"]
    if 'quality' in request.GET:
    	quality = int(request.GET["quality"])
    if 'crop' in request.GET:
    	crop = request.GET["crop"]

    try:
    	im = get_thumbnail(item.item_thumbnail, size, crop=crop, quality=quality)
    except:
    	return HttpResponse(status=500)

    return redirect(im.url)


def no_permission_redirect():
    return None
