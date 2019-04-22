from django import template


register = template.Library()


@register.inclusion_tag('selia/components/model_table.html')
def model_table(table):
    with_link = table.child.with_link | False
    fields = [field_name for field_name in table.child.fields]

    if with_link:
        data = [
            (datum, table.child.get_object_url(datum))
            for datum in table.data]
    else:
        data = zip(table.data, ["#" for _ in table.data])

    return {
        'data': data,
        'header': fields,
        'with_link': with_link,
    }
