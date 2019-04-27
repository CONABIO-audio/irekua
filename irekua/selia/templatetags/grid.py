from django import template


register = template.Library()


@register.inclusion_tag('selia/components/grid.html')
def grid(filter_form):
    return {
        'include_map': True,
        'include_table': True,
        'include_detail': True,
        'include_summary': True,
        'filter_form': filter_form,
    }
