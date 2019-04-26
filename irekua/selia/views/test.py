from django.shortcuts import render


def test(request):
    return render(request, 'selia/test.html')
