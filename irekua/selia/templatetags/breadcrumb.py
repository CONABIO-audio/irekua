from django import template
from django.urls import reverse


register = template.Library()


MAPPING = {
    'user': {
        'sites': 'Mis Sitios',
        'devices': 'Mis Dispositivos',
        'sampling_events': 'Mis Eventos de Muestreo',
        'items': 'Mis Items',
        '__name__': 'Mi Hogar',
    },
    'collections': {
        'sites': 'Sitios',
        'devices': 'Dispositivos',
        'sampling_events': 'Eventos de Muestreo',
        'items': 'Items',
        '__name__': 'Colecciones',
    },
    'sampling_events': {
        'sites': 'Sitios',
        'devices': 'Dispositivos',
        'items': 'Items',
        '__name__': 'Eventos de Muestreo',
    }
}


@register.inclusion_tag('selia/components/breadcrumb.html')
def breadcrumb(request):
    path_components = request.path.split('/')[1:-1]
    # data, current = get_paths(path_components)
    data = []
    current = ['Current']
    return {'data': data, 'current': current[0]}


def get_url(path_components):
    return '/' + '/'.join(path_components) + '/'


def get_single_node(path_components):
    tag = MAPPING[path_components[-1]]['__name__']
    path = get_url(path_components)
    return (tag, path)


def get_double_node(path_components):
    tag = MAPPING[path_components[-2]].get(path_components[-1], path_components[-1])
    url = get_url(path_components)

    pre_tag = MAPPING[path_components[-2]]['__name__']
    pre_url = get_url(path_components[:-1])
    return [(pre_tag, pre_url)], (tag, url)


def get_paths(path_components):
    path = '/' + '/'.join(path_components) + '/'
    last = path_components[-1]

    if len(path_components) == 2:
        current = get_single_node(path_components)
        return [], current

    if len(path_components) == 3:
        data, current = get_double_node(path_components)
        return data, current

    if last in MAPPING:
        data, current = get_paths(path_components[:-1])
        data.append(current)

        current = get_single_node(path_components)
        return data, current

    pre_last = path_components[-2]
    if pre_last not in MAPPING:
        msg = 'Breadcrumb not valid in this url : {}'.format(path)
        raise NotImplementedError(msg)

    data, pre_current = get_paths(path_components[:-2])
    new_data, current = get_double_node(path_components)
    data += [pre_current] + new_data
    return data, current
