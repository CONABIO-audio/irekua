from django.shortcuts import render

# Create your views here.
def collections(request):
    try:
        user = request.user
    except AttributeError:
        pass
    pass
