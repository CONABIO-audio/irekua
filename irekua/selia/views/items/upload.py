from django.shortcuts import render
from django import forms

from database import models


def upload_items(request):
    return render(request, 'selia/items/upload.html')
