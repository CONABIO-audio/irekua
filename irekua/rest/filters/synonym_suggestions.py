import django_filters

from database.models import SynonymSuggestion


class SynonymSuggestionFilter(django_filters.FilterSet):
    suggested_on__gt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')
    suggested_on__lt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')

    class Meta:
        model = SynonymSuggestion
        fields = (
            'source__term_type__name',
            'source__value',
            'synonym',
            'suggested_by__username',
            'suggested_by__first_name',
        )
