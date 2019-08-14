from django.shortcuts import render


def about_contact(request):
    return render(request, 'selia/about/contact.html')
