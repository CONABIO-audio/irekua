from django import template

register = template.Library()


@register.simple_tag
def show_json(data):
    return parse_json_value(data)


def parse_json_object(data):
    html_string = ''


def parse_json_list(data):
    pass


def parse_json_string(data):
    pass


def parse_json_number(data):
    pass


def parse_json_boolean(data):
    pass


def parse_json_null(data):
    pass


def parse_json_value(data):
    if isinstance(data, dict):
        return parse_json_object(data)

    if isinstance(data, (list, tuple)):
        return parse_json_list(data)

    if isinstance(data, str):
        return parse_json_string(data)

    if isinstance(data, (int, float)):
        return parse_json_number(data)

    if isinstance(data, bool):
        return parse_json_boolean(data)

    return parse_json_null(data)
