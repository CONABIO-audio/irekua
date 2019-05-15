from django.http import HttpResponseNotAllowed, HttpResponse


def update_session(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    for key, value in request.POST.items():
        request.session[key] = value

    return HttpResponse('ok')
