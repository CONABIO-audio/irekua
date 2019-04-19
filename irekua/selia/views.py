from django.shortcuts import render


def home(request):
    template = 'selia/home.html'

    if request.user.is_authenticated:
        template = 'selia/user_home.html'

    return render(request, template)


def about(request):
    return render(request, 'selia/about.html')
