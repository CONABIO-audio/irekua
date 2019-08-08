from selia.views.utils import SeliaAnnotationView
from database.models import Item
from database.models import Annotation

class CollectionItemAnnotatorView(SeliaAnnotationView):
    template_name = 'selia/item_detail/annotations/annotator.html'
    annotator_template = 'selia/components/annotators/image.html'
    model = Annotation
    success_url = 'selia:item_annotations'
    mode = 'create'

    fields = ["annotation_tool","item","event_type","label","annotation_type","annotation","annotation_configuration","certainty","quality","commentaries"]


