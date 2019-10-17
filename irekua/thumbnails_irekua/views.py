from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def upload(request):
    response = {'hola': 'adios'}

    return HttpResponse(
        response,
        content_type='application/json',
        status_code=201)
