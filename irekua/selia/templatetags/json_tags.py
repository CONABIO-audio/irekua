from django import template
from django.utils.html import format_html
from django.utils.translation import gettext as _

register = template.Library()


@register.simple_tag
def show_json(data):
    return parse_json_value(data, 0)


def parse_json_object(data, level):
    if level == 0:
        header_level = 'h5'
        div_class = 'd-block m-2 bg-light border rounded p-3 shadow-sm'
    else:
        header_level = 'h6'
        div_class = 'd-block'

    headers = [
        '''<div class="{div_class}">
             <{header_level}>{key}</{header_level}>
             <div class="container ml-4">{value}</div>
           </div>'''.format(
               key=key,
               value=parse_json_value(value, level + 1),
               header_level=header_level,
               div_class=div_class)
        for key, value in sorted(data.items())]

    return format_html(''.join(headers))


def parse_json_list(data, level):
    bullets = [
        '<li>{}</li>'.format(parse_json_value(value, level + 1))
        for value in data
    ]

    return '<ul>{}</ul>'.format(''.join(bullets))


def parse_json_string(data):
    return '<p class="text-muted">{}</p>'.format(data)


def parse_json_number(data):
    return '<p class="text-muted">{}</p>'.format(data)


def parse_json_boolean(data):
    if data:
        response = _('yes')
    else:
        response =  _('no')

    return '<p class="text-muted">{}</p>'.format(response)


def parse_json_null():
    return ''


def parse_json_value(data, level):
    if isinstance(data, dict):
        return parse_json_object(data, level)

    if isinstance(data, (list, tuple)):
        return parse_json_list(data, level)

    if isinstance(data, bool):
        return parse_json_boolean(data)

    if isinstance(data, str):
        return parse_json_string(data)

    if isinstance(data, (int, float)):
        return parse_json_number(data)

    return parse_json_null()
