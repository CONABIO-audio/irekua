from django import forms

from database.models import SamplingEvent
from database.models import SamplingEventType
from database.models import Collection
from database.models import CollectionSite

from irekua_utils.filters.data_collections import collection_sites as site_utils

from selia.forms.widgets import BootstrapDateTimePickerInput
from selia.forms.json_field import JsonField
from selia.views.utils import SeliaCreateView
from selia.views.utils import SeliaList


class SamplingEventCreateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = SamplingEvent
        fields = [
            'sampling_event_type',
            'collection_site',
            'metadata',
            'started_on',
            'ended_on',
            'collection'
        ]

        widgets = {
            'started_on': BootstrapDateTimePickerInput(),
            'ended_on': BootstrapDateTimePickerInput(),
        }


class SamplingEventCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/sampling_events/create.html'
    model = SamplingEvent
    success_url = 'selia:collection_sampling_events'
    form_class = SamplingEventCreateForm

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def handle_create(self):
        form = self.get_form()

        if form.is_valid():
            sampling_event = form.save(commit=False)
            sampling_event.created_by = self.request.user
            sampling_event.save()
            return self.handle_finish_create(sampling_event)

        self.object = None
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'collection_site' in self.request.GET:
            site_pk = self.request.GET['collection_site']
            initial['collection_site'] = CollectionSite.objects.get(pk=site_pk)

        if 'sampling_event_type' in self.request.GET:
            initial['sampling_event_type'] = SamplingEventType.objects.get(
                pk=self.request.GET['sampling_event_type'])

        return initial

    def get_site_list(self):
        class SiteList(SeliaList):
            prefix = 'sites'

            filter_class = site_utils.Filter
            search_fields = site_utils.search_fields
            ordering_fields = site_utils.ordering_fields

            queryset = CollectionSite.objects.filter(collection=self.collection)

            list_item_template = 'selia/components/select_list_items/collection_sites.html'
            filter_form_template = 'selia/components/filters/collection_site.html'

        site_list = SiteList()
        return site_list.get_context_data(self.request)

    def get_sampling_event_types(self):
        collection_type = self.collection.collection_type

        if collection_type.restrict_sampling_event_types:
            return collection_type.sampling_event_types.all()

        return SamplingEventType.objects.all()

    def get_sampling_event_type(self, context):
        sampling_event_types = context['sampling_event_types']
        if sampling_event_types.count() == 1:
            return sampling_event_types.first()

        if 'sampling_event_type' in self.request.GET:
            sampling_event_type = SamplingEventType.objects.get(
                pk=self.request.GET['sampling_event_type'])
            return sampling_event_type

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        self.collection = self.get_object(queryset=Collection.objects.all())
        context['collection'] = self.collection
        context['site_list'] = self.get_site_list()
        context['sampling_event_types'] = self.get_sampling_event_types()

        if 'collection_site' in self.request.GET:
            collection_site = CollectionSite.objects.get(pk=self.request.GET['collection_site'])
            context['collection_site'] = collection_site

        sampling_event_type = self.get_sampling_event_type(context)
        context['sampling_event_type'] = sampling_event_type

        if sampling_event_type:
            context['form'].fields['metadata'].update_schema(
                sampling_event_type.metadata_schema)
        return context
