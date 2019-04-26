from django.shortcuts import render
from django import forms
from django.db import models
from database.models import Item

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_type', 'item_file', 'created_by', 'sampling_event_device'  # 'captured_on', 'licence',
        )
