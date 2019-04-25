from django.shortcuts import render
from django import forms

from django.conf import settings
from django.core.files.storage import FileSystemStorage

class NameForm(forms.Form):
    file = forms.FileField()


def file_upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES['item']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)

    form = NameForm()
    return render(request, 'selia/upload.html', {'form': form})
