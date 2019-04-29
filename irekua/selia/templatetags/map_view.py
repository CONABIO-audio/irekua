from django import template


register = template.Library()


@register.inclusion_tag('selia/components/views/map.html')
def map_view(map_info):
    return map_info
