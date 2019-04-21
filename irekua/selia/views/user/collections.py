from django.shortcuts import render


def user_collections(request):
    return render(request, 'selia/user/collections.html')
