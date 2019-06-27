from django import forms
from django.views.generic import ListView
from django.utils.translation import gettext as _

from .search_filter import SearchFilter


class SearchForm(forms.Form):
    search = forms.CharField(
        label=_('search'),
        max_length=100,
        required=False)


class SeliaListView(ListView):
    paginate_by = 10
    empty_message = _('Empty list')

    def get_search_form(self):
        form = SearchForm(self.request.GET)
        return form

    def get_ordering_choices(self):
        orderings = []
        for field, label in self.ordering_fields:
            orderings.append(
                (
                    field,
                    '{order} {label}'.format(
                        label=label, order=_('↑'))
                )
            )

            orderings.append(
                (
                    '-{field}'.format(field=field),
                    '{order} {label}'.format(
                        label=label, order=_('↓'))
                )
            )

        return orderings

    def get_ordering_form(self):
        ordering_choices = self.get_ordering_choices()

        class OrderingForm(forms.Form):
            order = forms.ChoiceField(
                label=_('ordering'),
                choices=ordering_choices)

        ordering_form = OrderingForm(self.request.GET)
        return ordering_form

    def get_filter_class(self):
        if hasattr(self, 'filter_class'):
            return self.filter_class

        raise NotImplementedError('No filter class was provided')

    def get_initial_queryset(self):
        if hasattr(self, 'queryset'):
            return self.queryset

        raise NotImplementedError('No initial queryset was provided')

    def get_queryset(self):
        queryset = self.get_initial_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        return filtered_queryset

    def filter_queryset_with_query(self, queryset):
        if hasattr(self, 'filter_class'):
            filter_class = self.get_filter_class()
            self.filter = filter_class(self.request.GET, queryset=queryset)
            queryset = self.filter.qs

        return queryset

    def filter_queryset_with_search(self, queryset):
        if hasattr(self, 'search_fields'):
            self.search_form = self.get_search_form()

            if self.search_form.is_valid():
                queryset = SearchFilter().filter_queryset(self.request, queryset, self)

        return queryset

    def order_queryset(self, queryset):
        if hasattr(self, 'ordering_fields'):
            self.order_form = self.get_ordering_form()

            if self.order_form.is_valid():
                ordering = self.order_form.data['order']
                queryset = queryset.order_by(ordering)

        return queryset

    def filter_queryset(self, queryset):
        queryset = self.filter_queryset_with_query(queryset)
        queryset = self.filter_queryset_with_search(queryset)
        self.queryset = self.order_queryset(queryset)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context = {
            'object_list': context,
            'empty_message': self.empty_message
        }

        if hasattr(self, 'filter'):
            new_context['filter'] = self.filter

        if hasattr(self, 'search_form'):
            new_context['search_form'] = self.search_form

        if hasattr(self, 'order_form'):
            new_context['order_form'] = self.order_form

        return new_context
