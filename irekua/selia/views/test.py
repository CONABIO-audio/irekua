from django.shortcuts import render
from django import forms

class NameForm(forms.Form):
    file = forms.FileField()


def file_upload(request):
    if request.method == "POST":
        print(request.FILES)
    form = NameForm()
    return render(request, 'selia/test.html', {'form': form})
