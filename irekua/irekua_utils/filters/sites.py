from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet, DateFilter

from database.models import Site


class Filter(FilterSet):
    class Meta:
        model = Site

        fields = {
            'name': ['exact', 'icontains'],
            'locality': ['exact', 'icontains'],
            'latitude': ['gt', 'lt'],
            'longitude': ['gt', 'lt'],
            'altitude': ['gt', 'lt'],
            'created_on': ['gt', 'lt']
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            }
        }

search_fields = (
    'name',
    'locality',
)


ordering_fields = (
    ('created_on', _('added on')),
    ('name', _('name')),
    ('locality', _('locality')),
)
