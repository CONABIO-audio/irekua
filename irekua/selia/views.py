from django.shortcuts import render


def home(request):
    return render(request, 'selia/home.html')


def user_home(request):
    return render(request, 'selia/user_home.html')


def about(request):
    return render(request, 'selia/about.html')
