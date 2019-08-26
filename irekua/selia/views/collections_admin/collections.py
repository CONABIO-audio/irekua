from django.db import models
from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet
from django_filters import ModelChoiceFilter
from django_filters import DateFilter
from dal import autocomplete

from database.models import Collection
from database.models import Institution
from selia.views.list_views.base import SeliaListView


class ManagedCollectionsView(SeliaListView):
    template_name = 'selia/collections_admin/managed_collections.html'
    list_item_template = 'selia/components/list_items/managed_collection.html'
    help_template = 'selia/components/help/managed_collections.html'
    filter_form_template = 'selia/components/filters/managed_collection.html'

    search_fields = (
        'name',
        'collection_type__name',
        'institution__institution_name'
    )

    ordering_fields = (
        ('created_on', _('created on')),
    )

    def get_initial_queryset(self):
        user = self.request.user
        collection_types = user.collectiontype_set.all()
        return Collection.objects.filter(collection_type__in=collection_types)

    def get_filter_class(self):
        user = self.request.user

        def get_extra(f):
            urls = {
                'collection type': 'selia:collection_type_autocomplete',
                'institution': 'selia:institutions_autocomplete',
            }
            querysets = {
                'collection type': user.collectiontype_set.all(),
                'institution': Institution.objects.all(),
            }

            extra = {
                'queryset': querysets[f.verbose_name],
                'widget': autocomplete.ModelSelect2(
                    url=urls[f.verbose_name],
                    attrs={'style': 'width:100%'})
            }
            return extra

        class Filter(FilterSet):
            class Meta:
                model = Collection
                fields = {
                    'collection_type': ['exact'],
                    'institution': ['exact'],
                    'institution__institution_name': ['icontains'],
                    'institution__institution_code': ['icontains'],
                    'created_on': ['gt', 'lt'],
                    'is_open': ['exact'],
                }

                filter_overrides = {
                    models.ForeignKey: {
                        'filter_class': ModelChoiceFilter,
                        'extra': get_extra,
                    },
                    models.DateTimeField: {
                        'filter_class': DateFilter,
                        'extra': lambda f: {
                            'widget': forms.DateInput(
                                attrs={'class': 'datepicker'}
                            )
                        }
                    }
                }

        return Filter
