from django.http import HttpResponseNotAllowed, HttpResponse



def upload_file(request):
    if request.method == 'POST':
        return HttpResponse('OK')

    return HttpResponseNotAllowed(['POST'])
