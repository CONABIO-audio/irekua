from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaCreateView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import Item

class SamplingEventDeviceItemCreateView(SeliaCreateView):
    template_name = 'selia/sampling_event_device_detail/items/create.html'
    model = Item
    success_url = 'selia:sampling_event_device_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]

    def get_success_url_args(self):
        return [self.kwargs['pk']]
        
    def get_sampling_event_device_list(self):
        queryset = SamplingEventDevice.objects.filter(sampling_event__pk=self.kwargs['pk'])
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)

        return page

    def handle_create(self):
        form = self.get_form()
        print(form.data)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = self.request.user
            item.save()
            return self.handle_finish_create(item)
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def get_initial(self):
        initial = {
            'sampling_event_device': SamplingEventDevice.objects.get(pk=self.kwargs['pk'])
        }

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event_device'] = self.get_object(queryset=SamplingEventDevice.objects.all())

        return context
