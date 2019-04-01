import django_filters

from database.models import Site
from .utils import BaseFilter


class SiteFilter(BaseFilter):
    latitude__gt = django_filters.NumberFilter(
        field_name='latitude',
        lookup_expr='gt')
    latitude__lt = django_filters.NumberFilter(
        field_name='latitude',
        lookup_expr='lt')

    longitude__gt = django_filters.NumberFilter(
        field_name='longitude',
        lookup_expr='gt')
    longitude__lt = django_filters.NumberFilter(
        field_name='longitude',
        lookup_expr='lt')

    altitude__gt = django_filters.NumberFilter(
        field_name='altitude',
        lookup_expr='gt')
    altitude__lt = django_filters.NumberFilter(
        field_name='altitude',
        lookup_expr='lt')

    class Meta:
        model = Site
        fields = (
            'name',
            'site_type__name',
            'locality',
            'creator',
        )
