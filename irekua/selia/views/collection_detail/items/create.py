from django import forms
from django.shortcuts import redirect
from selia.views.utils import SeliaCreateView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ValidationError
from database.models import SamplingEventDevice
from database.models import SamplingEvent
from database.models import Collection
from database.models import Item
import json
from ast import literal_eval


class CollectionItemCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/items/create.html'
    model = Item
    success_url = 'selia:collection_items'
    fields = ["item_type","item_file","sampling_event_device","source","captured_on","licence","tags"]

    def get_items_in_list(self,pk_list):
        queryset = Item.objects.filter(pk__in=pk_list)
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)
        return page

    def get(self, *args, **kwargs):
        if 'success_pks' in self.request.GET:
            self.object = None
            context = self.get_context_data()
            
            successes = literal_eval(self.request.GET["success_pks"])
            duplicates = literal_eval(self.request.GET["duplicate_pks"])

            context["success_list"] = self.get_items_in_list(successes)
            context["duplicate_list"] = self.get_items_in_list(duplicates)
            context["success_count"] = len(successes)
            context["duplicate_count"] = len(duplicates)

            return self.render_to_response(context)
        else:
            return super().get(*args, **kwargs)            

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def get_sampling_event_list(self):
        queryset = SamplingEvent.objects.filter()
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)

        return page

    def get_sampling_event_device_list(self):
        if 'sampling_event' in self.request.GET:
            sampling_event = self.request.GET.get('sampling_event', None)
            queryset = SamplingEventDevice.objects.filter(sampling_event__pk=sampling_event)
            paginator = Paginator(queryset,5)
            page = self.request.GET.get('page',1)
            page = paginator.get_page(page)

            return page
        else:
            return EmptyPage()


    def get_back_url(self):
        if 'back' in self.request.GET:
            chain_str = self.get_chain()
            back_url = self.request.GET['back']+"?"

            if 'sampling_event' in self.request.GET and 'sampling_event_device' in self.request.GET:
                back_url = back_url + "sampling_event="+self.request.GET["sampling_event"]+"&"

            return back_url+"chain="+chain_str
        elif 'sampling_event' in self.request.GET:
            return reverse('selia:collection_item_create', args=[self.kwargs['pk']])
        else:
            chain_str, next_url = self.get_new_chain()

            if next_url == '':
                return self.get_success_url()

            return next_url+"?chain="+chain_str
            

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = self.request.user
            try:
                item.save()
            except ValidationError:
                item_hash = item.hash
                duplicate = Item.objects.filter(hash=item_hash)

                if duplicate:
                    error_data = {
                    'error_type': 'duplicate',
                    'duplicate_pk':duplicate[0].pk
                    }

                    return HttpResponse(json.dumps(error_data), content_type="application/json",status=400)

            if 'async' in self.request.GET:
                success_data = {
                'success_pk': item.pk
                }
                return HttpResponse(json.dumps(success_data), content_type="application/json")
            else:
                return self.handle_finish_create(item)
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form

            return self.render_to_response(context)

    def get_initial(self):
        initial = {
            'collection': Collection.objects.get(pk=self.kwargs['pk'])
        }

        if 'sampling_event' in self.request.GET:
            initial['sampling_event'] = SamplingEvent.objects.get(pk=self.request.GET['sampling_event'])
        if 'sampling_event_device' in self.request.GET:
            initial['sampling_event_device'] = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])           

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.get_object(queryset=Collection.objects.all())
        context['sampling_event_list'] = self.get_sampling_event_list()
        context['sampling_event_device_list'] = self.get_sampling_event_device_list()

        if 'sampling_event' in self.request.GET:
            sampling_event = SamplingEvent.objects.get(pk=self.request.GET['sampling_event'])
            context['selected_sampling_event'] = sampling_event

        if 'sampling_event_device' in self.request.GET:
            sampling_event_device = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])
            context['selected_sampling_event_device'] = sampling_event_device


        return context
