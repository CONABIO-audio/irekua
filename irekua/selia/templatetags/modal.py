from django import template


register = template.Library()


@register.tag(name='modal')
def do_modal(parser, token):
    nodelist = parser.parse(('endmodal',))
    parser.delete_first_token()
    return ModalNode(nodelist)


class ModalNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return ''
