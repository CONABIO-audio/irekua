from django.shortcuts import render
from django import forms

from selia.forms.json_field import JsonField

from database.models import Collection



class CollectionForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Collection
        fields = [
            'name',
            'description',
            'institution',
            'metadata',
        ]


def test(request):
    collection = Collection.objects.first()
    collection_type = collection.collection_type
    metadata_schema = collection_type.metadata_schema

    if request.method.lower() == 'post':
        print(request.POST)

    form = CollectionForm(instance=collection)
    form.fields['metadata'].update_schema(metadata_schema)

    context = {'form': form}
    return render(request, 'selia/test.html', context=context)
