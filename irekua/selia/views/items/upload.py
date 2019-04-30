from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


def handle_files(files):
    for tempfile in files:
        print(type(tempfile))



def upload_items(request):
    if request.method == "POST":
        handle_files(request.FILES.getlist('file_field'))
        return HttpResponseRedirect('#')

    context = {'form': FileFieldForm()}
    return render(request, 'selia/items/upload.html', context)
