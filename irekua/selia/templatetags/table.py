from django import template


register = template.Library()


@register.inclusion_tag('selia/components/views/table.html')
def table(table_info):
    return {}
