from django.views.generic import TemplateView
from django.forms import ModelForm


from database import models


class TestForm(ModelForm):
    class Meta:
        model = models.SamplingEvent
        fields = (
            'sampling_event_type',
            'collection_site',
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
            'collection',
            'licence',
        )


class TestView(TemplateView):
    template_name = 'selia/test.html'

    def get_context_data(self):
        form = TestForm()
        return {
            'form': form
        }


