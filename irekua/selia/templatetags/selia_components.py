from django import template
from dal_select2.widgets import Select2WidgetMixin

register = template.Library()


@register.inclusion_tag('selia/components/list.html', takes_context=True)
def list_component(context, template_name, item_list, empty_message):
    context['template_name'] = template_name
    context['item_list'] = item_list
    context['empty_message'] = empty_message
    return context


@register.inclusion_tag('selia/components/detail.html', takes_context=True)
def detail_component(context, detail_template, object):
    context['detail_template'] = detail_template
    context['object'] = object
    return context


@register.inclusion_tag('selia/components/help.html', takes_context=True)
def help_component(context, help_template):
    context['help_template'] = help_template
    return context


@register.inclusion_tag('selia/components/update.html', takes_context=True)
def update_component(context, update_template, form):
    context['update_template'] = update_template
    context['form'] = form
    return context


@register.inclusion_tag('selia/components/summary.html', takes_context=True)
def summary_component(context, summary_template, object):
    context['summary_template'] = summary_template
    context['object'] = object
    return context


@register.inclusion_tag('selia/components/filter.html', takes_context=True)
def filter_component(context, filter_template, filter):
    context['filter_template'] = filter_template
    context['filter'] = filter
    return context


@register.inclusion_tag('selia/components/delete.html', takes_context=True)
def delete_component(context, object):
    context['object'] = object
    return context


@register.inclusion_tag('selia/components/create.html', takes_context=True)
def create_component(context, create_template, form):
    context['create_template'] = create_template
    context['form'] = form
    return context


@register.simple_tag
def autocomplete_media():
    return Select2WidgetMixin().media
