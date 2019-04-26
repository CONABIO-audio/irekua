from django import template


register = template.Library()


@register.inclusion_tag('selia/components/views/detail.html')
def detail(detail_info):
    return {}
