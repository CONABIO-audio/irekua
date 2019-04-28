from django import template


register = template.Library()


@register.inclusion_tag('selia/components/grid.html')
def grid(grid_config, table_info, map_info):
    return {
        'grid_config': grid_config,
        'table_info': table_info,
        'map_info': map_info,
    }
