from django import template

register = template.Library()


@register.inclusion_tag('selia/components/buttons/help.html')
def help_button():
    return {}


@register.inclusion_tag('selia/components/buttons/see.html')
def see_button():
    return {}


@register.inclusion_tag('selia/components/buttons/enter.html')
def enter_button():
    return {}


@register.inclusion_tag('selia/components/buttons/add.html')
def add_button():
    return {}


@register.inclusion_tag('selia/components/buttons/update.html')
def update_button():
    return {}


@register.inclusion_tag('selia/components/buttons/edit.html')
def edit_button():
    return {}
