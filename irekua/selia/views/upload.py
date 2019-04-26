from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django import forms

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import PhotoForm
from database.models import Item

class NameForm(forms.Form):
    file = forms.FileField()


def upload(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES['item']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    form = NameForm()
    # return render(request, 'selia/upload.html', {'form': form})
    return render(request, 'selia/upload.html', context)

def photo_list(request):
    photos = Item.objects.all()
    return render(request, 'selia/photo_list.html', {
        'photos': photos
        })

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('selia:photo_list')
    else:
        form = PhotoForm()
    return render(request, 'selia/upload_photo.html',{
        'form': form
    })