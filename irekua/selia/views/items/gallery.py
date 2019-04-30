from django.shortcuts import render


def gallery(request):
    return render(request, 'selia/items/gallery.html')
