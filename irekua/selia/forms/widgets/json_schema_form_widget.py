from django.forms.widgets import Widget
import json


class JsonSchemaFormWidget(Widget):
    template_name = 'selia/widgets/json_form_widget.html'
    input_type = 'text'

    def format_value(self, value):
        return json.dumps(value)
