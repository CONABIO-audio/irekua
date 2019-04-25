from django import template


register = template.Library()


@register.inclusion_tag('selia/components/generic_detail.html')
def generic_detail(serialized_object):
    return {'serialized_object': serialized_object}
