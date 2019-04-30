from django.http import HttpResponse
from django import forms
from django.shortcuts import render


import database.models as db_models

class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = db_models.Site
        fields = ['name','locality','site_type','altitude','metadata']

class PhysicalDeviceUpdateForm(forms.ModelForm):
    class Meta:
        model = db_models.PhysicalDevice
        fields = ['serial_number','metadata']

class SamplingEventUpdateForm(forms.ModelForm):
    class Meta:
        model = db_models.SamplingEvent
        fields = ['commentaries','metadata','started_on','ended_on']

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = db_models.Item
        fields = ['metadata']

FORM_CLASSES = {
        "Site" : SiteUpdateForm,
        "SamplingEvent" : SamplingEventUpdateForm,
        "Item" : ItemUpdateForm,
        "PhysicalDevice" : PhysicalDeviceUpdateForm
}


def UserFormCreator(request, id, model_name):
    #if request.is_ajax():
    model = getattr(db_models, model_name)
    instance = model.objects.get(id=id)
    data = {}
    for fKey in FORM_CLASSES[model_name].Meta.fields:
        data[fKey] = getattr(instance,fKey)

    form = FORM_CLASSES[model_name](initial=data)

    return render(request,"selia/user/components/update_form.html",{"form":form})
    #else:
    #    pass

     

