from django.shortcuts import render


# Create your views here.
def home(request):
    template = 'selia/home.html'

    if request.user.is_authenticated:
        template = 'selia/user_home.html'

    return render(request, template)
