import django_filters

from database.models import TermSuggestion


search_fields = (
    'value',
)


class Filter(django_filters.FilterSet):
    suggested_on__gt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')
    suggested_on__lt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')

    class Meta:
        model = TermSuggestion
        fields = (
            'value',
            'suggested_by__username',
            'suggested_by__first_name',
            'suggested_by__is_superuser',
            'suggested_by__is_curator'
        )
