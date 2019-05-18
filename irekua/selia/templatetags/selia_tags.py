from django import template
from django.template import Context


register = template.Library()


@register.tag(name='card')
def card(parser, token):
    nodelist = parser.parse(('endcard',))
    parser.delete_first_token()
    return CardNode(nodelist)


@register.tag(name='card_body')
def card_body(parser, token):
    nodelist = parser.parse(('endcard_body',))
    parser.delete_first_token()
    return CardNode(nodelist)


@register.tag(name='card_header')
def card_header(parser, token):
    nodelist = parser.parse(('endcard_header',))
    parser.delete_first_token()
    return CardNode(nodelist)


@register.tag(name='card_footer')
def card_footer(parser, token):
    nodelist = parser.parse(('endcard_footer',))
    parser.delete_first_token()
    return CardNode(nodelist)


class BaseNode(template.Node):
    template_name = ''

    def __init__(self, nodelist, extra_classes=''):
        self.nodelist = nodelist
        self.extra_classes = extra_classes

    def render(self, context):
        card_template = self.get_template(context)
        content = self.get_content(context)
        card_context = self.get_context(content)
        return card_template.render(card_context)

    def get_content(self, context):
        return self.nodelist.render(context)

    def get_context(self, content):
        context = {'content': content}
        return Context(context)

    def get_template(self, context):
        return context.template.engine.get_template(self.template_name)


class CardNode(BaseNode):
    template_name = 'selia/components/card.html'


class CardBodyNode(BaseNode):
    template_name = 'selia/components/card_body.html'


class CardHeaderNode(BaseNode):
    template_name = 'selia/components/card_header.html'


class CardFooterNode(BaseNode):
    template_name = 'selia/components/card_footer.html'
