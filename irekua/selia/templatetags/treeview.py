from collections import OrderedDict
from django import template
from django.urls import resolve, reverse
from django.utils.translation import gettext as _


register = template.Library()


TREE_DATA = OrderedDict({
    'user_home': (_('Home'), None, None),
    'user_devices': (_('My Devices'), 'user_home', None),
    'user_sites': (_('My Sites'), 'user_home', None),
    'user_items': (_('My Items'), 'user_home', None),
    'user_sampling_events': (_('My Sampling Events'), 'user_home', None),
    'collections': (_('Collections'), None, None),
    'open_collections': (_('Open Collections'), None, None),
    'collection_home': (None, 'collections', 'collection_name'),
    'collection_devices': (_('Collection Devices'), 'collection_home', None),
    'collection_sites': (_('Collection Sites'), 'collection_home', None),
    'collection_items': (_('Collection Items'), 'collection_home', None),
    'collection_sampling_events': (_('Collection Sampling Events'),
        'collection_home', None),
    'sampling_event_home': (None, 'collection_sampling_events',
        'sampling_event_id'),
    'sampling_event_devices': (_('Sampling Event Devices'),
        'sampling_event_home', None),
    'sampling_event_items': (_('Sampling Event Items'),
        'sampling_event_home', None),
    'sampling_event_device_home': (None, 'sampling_event_devices', 'sampling_event_device_id'),
    'sampling_event_device_items': (_('Sampling Event Device Items'), 'sampling_event_device_home', None),
})


class Node():
    def __init__(self, name, url_name, parent, kwarg_name):
        self.name = name
        self.url_name = url_name
        self.parent = parent
        self.kwarg_name = kwarg_name

        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        return self.url_name == other.url_name

    def is_child(self, other):
        if self.parent is None:
            return False

        if self.parent == other:
            return True

        return self.parent.is_child(other)

    def is_sibling(self, other):
        return self.parent == other.parent

    def get_kwargs(self):
        if self.parent is None:
            return []

        kwargs = self.parent.get_kwargs()
        if self.kwarg_name is not None:
            kwargs.append(self.kwarg_name)

        return kwargs

    def get_name(self, view):
        if self.name is None:
            return view.kwargs[self.kwarg_name]
        return self.name

    def get_url(self, view):
        kwargs = {
            key: value for key, value in view.kwargs.items()
            if key in self.get_kwargs()
        }
        return reverse('selia:' + self.url_name, kwargs=kwargs)


class Tree():
    def __init__(self):
        self.nodes = OrderedDict({})

    def get_node(self, node_name):
        return self.nodes.get(node_name, None)

    def add_node(self, node):
        self.nodes[node.url_name] = node

    def get_subtree(self, name):
        leaf_node = self.get_node(name)

        subtree = OrderedDict({
            key: value for key, value in self.nodes.items()
            if (
                value == leaf_node or
                leaf_node.is_child(value) or
                leaf_node.is_sibling(value)
            )
        })
        return subtree


def build_tree():
    tree = Tree()

    for key, (name, parent, kwarg_name) in TREE_DATA.items():
        if parent is not None:
            parent = tree.get_node(parent)

        node = Node(name, key, parent, kwarg_name)
        tree.add_node(node)

    return tree


TREE = build_tree()


@register.inclusion_tag('selia/components/treeview.html')
def treeview(request):
    path = request.path
    view = resolve(path)

    try:
        tree = TREE.get_subtree(view.url_name)
        tree_data = [
            (node.get_name(view), node.get_url(view), range(node.depth)) for node in tree.values()
        ]
    except:
        tree_data = []

    return {'tree': tree_data, 'request': request}
