from django import template


register = template.Library()


@register.inclusion_tag('selia/components/grid.html')
def grid(grid_info):
    return {
        'include_map': True,
        'include_table': True,
        'include_detail': True,
        'include_summary': True,
    }
