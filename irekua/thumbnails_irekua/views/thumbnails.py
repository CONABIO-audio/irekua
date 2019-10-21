from django.http import HttpResponse
from django.views.decorators.http import require_GET

from irekua_utils.permissions.items import items as permissions


@require_GET
def generate_thumbnail(request):
    if not permissions.view_thumbnail(request.user):
        return no_permission_redirect()

    return HttpResponse(status=200)


def no_permission_redirect():
    return None
