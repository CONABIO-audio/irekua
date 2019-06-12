from django.shortcuts import render


def home(request):
    return render(request, 'irekua/home.html')


def about(request):
    return render(request, 'irekua/about.html')


def contact(request):
    return render(request, 'irekua/contact.html')
