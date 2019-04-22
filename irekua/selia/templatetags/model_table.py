from django import template


register = template.Library()


@register.inclusion_tag('selia/components/model_table.html')
def model_table(table):
    fields = [field_name for field_name in table.child.fields]
    data = table.data
    return {'data': data, 'header': fields}
