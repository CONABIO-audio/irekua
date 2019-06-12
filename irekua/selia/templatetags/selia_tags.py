from django import template
from django.template import Context


register = template.Library()


@register.tag(name='component')
def component(parser, token):
    name, extra_classes, style = get_component_info(token)
    template = get_template(name)

    nodelist = parser.parse(('endcomponent',))
    parser.delete_first_token()
    return ComponentNode(nodelist, template, extra_classes, style)


def get_component_info(token):
    contents = token.split_contents()

    try:
        name = contents[1]
    except IndexError:
        msg = 'Component tag does contain the name of the component'
        raise ValueError(msg)

    extra_classes, style = get_extra_classes_and_style(contents[2:])
    return name, extra_classes, style


def get_extra_classes_and_style(tokens):
    extra_classes = ''
    style = ''

    for token in tokens:
        try:
            key, value = token.split('=')
        except KeyError:
            msg = 'Only valid extra kwargs are "class" and "style"'
            raise ValueError(msg)

        if key == 'class':
            extra_classes = value[1:-1]

        elif key == 'style':
            style = value[1:-1]

        else:
            msg = 'Only valid extra kwargs are "class" and "style"'
            raise ValueError(msg)

    return extra_classes, style



TEMPLATE_HOME = 'selia/components'
def get_template(name):
    if name == 'card':
        template_name = 'card.html'
    elif name == 'card_body':
        template_name = 'card_body.html'
    elif name == 'card_footer':
        template_name = 'card_footer.html'
    elif name == 'card_header':
        template_name = 'card_header.html'
    else:
        msg = 'Component with name %s does no exists'
        raise NotImplementedError(msg % name)

    return '{home}/{name}'.format(home=TEMPLATE_HOME, name=template_name)



class ComponentNode(template.Node):
    def __init__(self, nodelist, template, extra_classes, style):
        self.nodelist = nodelist

        self.template = template
        self.extra_classes = extra_classes
        self.style = style

    def render(self, context):
        card_template = self.get_template(context)
        content = self.get_content(context)
        card_context = self.get_context(content)
        return card_template.render(card_context)

    def get_content(self, context):
        return self.nodelist.render(context)

    def get_context(self, content):
        context = {
            'content': content,
            'extra_classes': self.extra_classes,
            'style': self.style
        }
        return Context(context)

    def get_template(self, context):
        return context.template.engine.get_template(self.template)
