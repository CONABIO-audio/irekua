from django.shortcuts import render


def about(request):
    return render(request, 'selia/about.html')
