from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='registration:login')
def create_collection(request):
    return render(request, 'selia/collections/base.html')
