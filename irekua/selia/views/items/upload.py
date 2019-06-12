from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django import forms

from database import models


class UploadItems(TemplateView):
    template_name = 'selia/items/upload.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        context = super().get_context_data(**kwargs)

        context['sampling_event'] = self.get_sampling_event_context()
        return context

    def get_sampling_event_context(self):
        sampling_event, has_sampling_event = self.get_sampling_event()

        if has_sampling_event:
            return {}

        search_context = self.get_select_sampling_event_context()
        return {
            'search': search_context
        }

    def get_select_sampling_event_context(self):
        return self.get_search_sampling_event_context()

    def get_search_sampling_event_context(self):
        form = self.get_search_sampling_event_form()
        return {
            'show': True,
            'form': form
        }

    def get_sampling_event(self):
        sampling_event_id = self.request.GET.get('sampling_event_id', None)

        if sampling_event_id is not None:
            sampling_event = get_object_or_404(
                models.SamplingEvent,
                pk=sampling_event_id)
            return sampling_event, True
        else:
            return None, False

    def get_collection(self):
        collection_name = self.kwargs['collection_name']
        return get_object_or_404(models.Collection, pk=collection_name)

    def get_search_sampling_event_form(self):
        collection = self.get_collection()

        class SearchForm(forms.Form):
            site = forms.CharField(
                label='Site',
                max_length=100)
            date_field = forms.DateField(
                label='Date',
                widget=forms.TextInput(attrs={'id': 'datepicker'}))

        return SearchForm()
