from django import template


register = template.Library()


@register.inclusion_tag('selia/components/views/summary.html')
def summary(summary_info):
    return {}
