from django.shortcuts import render


def annotate(request):
    return render(request, 'selia/items/annotate.html')
