from django import forms

from database.models import SamplingEvent
from selia.views.components.grid import GridView
from rest.filters.sampling_events import Filter

from database.models import Collection


class UpdateForm(forms.ModelForm):
    class Meta:
        model = SamplingEvent
        fields = [
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
        ]



class CollectionSamplingEvents(GridView):
    template_name = 'selia/collections/detail/sampling_events.html'
    table_view_name = 'rest-api:collection-sampling-events'
    map_view_name = 'rest-api:collection-sampling-event-locations'
    filter_class = Filter
    update_form = UpdateForm

    with_table_links = True
    child_view_name = 'selia:sampling_event_home'

    update_form_url = '/selia/widgets/update_form/SamplingEvent/'

    def get_table_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_map_url_kwargs(self):
        collection_name = self.kwargs['collection_name']
        return {"pk": collection_name}

    def get_context_data(self, *args, **kwargs):
        collection = Collection.objects.get(pk=kwargs['collection_name'])

        class CreateForm(forms.ModelForm):
            licence = forms.ModelChoiceField(
                queryset=collection.licence_set.all())
            collection_site = forms.ModelChoiceField(
                queryset=collection.collectionsite_set.all())
            sampling_event_type = forms.ModelChoiceField(
                queryset=collection.collection_type.sampling_event_types.all())

            class Meta:
                model = SamplingEvent
                fields = [
                    'sampling_event_type',
                    'collection_site',
                    'commentaries',
                    'metadata',
                    'started_on',
                    'ended_on',
                    'licence',
                ]

        context = super().get_context_data()
        context['collection_name'] = kwargs['collection_name']
        context['create_form'] = CreateForm()
        return context
