from django import forms
from .base import SeliaAnnotationView
from database.models import Annotation


class BootstrapRadioSelect(forms.RadioSelect):
    template_name = 'selia/widgets/bootstrap_radio.html'


class AnnotationCreateForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = [
            "annotation_tool",
            "item",
            "event_type",
            "label",
            "annotation_type",
            "annotation",
            "annotation_configuration",
            "certainty",
            "quality",
            "commentaries"
        ]
        widgets = {
            "certainty": BootstrapRadioSelect,
            "quality": BootstrapRadioSelect
        }


class CollectionItemAnnotatorView(SeliaAnnotationView):
    template_name = 'selia/annotations/annotator.html'
    annotator_template = 'selia/components/annotators/image.html'
    success_url = 'selia:item_annotations'
    mode = 'create'

    model = Annotation
    form_class = AnnotationCreateForm

