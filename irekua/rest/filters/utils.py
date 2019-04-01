from django import forms
import django_filters


class BaseFilter(django_filters.FilterSet):
    created_on__lt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='lt',
        widget=forms.DateTimeInput)
    created_on__gt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt',
        widget=forms.DateTimeInput)
    modified_on__lt = django_filters.DateTimeFilter(
        field_name='modified_on',
        lookup_expr='lt',
        widget=forms.DateTimeInput)
    modified_on__gt = django_filters.DateTimeFilter(
        field_name='modified_on',
        lookup_expr='gt',
        widget=forms.DateTimeInput)
