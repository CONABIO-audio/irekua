from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet
from django_filters import CharFilter
from django_filters import DateFilter
from django_filters import ModelChoiceFilter

from dal import autocomplete

from database.models import Collection


class Filter(FilterSet):

    class Meta:
        model = Collection
        fields = {
            'collection_type': ['exact'],
            'name': ['icontains'],
            'institution': ['exact'],
            'institution__institution_name': ['exact', 'icontains'],
            'institution__institution_code': ['exact', 'icontains'],
            'institution__country': ['icontains'],
            'is_open': ['exact'],
            'created_on': ['gt', 'lt'],
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            },
            models.ForeignKey: {
                'filter_class': ModelChoiceFilter,
                'extra': lambda f: {
                    'queryset': f.target_field.model.objects.all(),
                    'widget': autocomplete.ModelSelect2(
                        url=f.target_field.model.autocomplete_url
                    )
                }
            }
        }


search_fields = (
    'name',
    'collection_type__name',
    'institution__institution_name',
    'institution__institution_code'
)


ordering_fields = (
    ('created_on', _('created on')),
    ('name', _('name'))
)
