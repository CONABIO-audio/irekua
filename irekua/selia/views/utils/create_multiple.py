from django import forms
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from database.models import Item, UploadSession, UploadEvent
import json
from ast import literal_eval
from .create_base import SeliaCreateView


class CreateUploadSessionForm(forms.ModelForm):
    class Meta:
        model = UploadSession
        fields = [
            'sampling_event_device'
        ]

class CreateUploadEventForm(forms.ModelForm):
    class Meta:
        model = UploadEvent
        fields = [
            'upload_session',
            'error',
            'item'
        ]

class SeliaMultipleItemsCreateView(SeliaCreateView):

class SeliaMultipleItemsCreateView(SeliaCreateView):
    def get_items_in_list(self,pk_list):
        queryset = Item.objects.filter(pk__in=pk_list)
        paginator = Paginator(queryset,5)
        page = self.request.GET.get('page',1)
        page = paginator.get_page(page)
        return page

    def get(self, *args, **kwargs):
        if 'get_session' in self.request.GET:
            sampling_event_device = SamplingEventDevice.objects.get(pk=self.request.GET['sampling_event_device'])
            upload_session_form = CreateUploadSessionForm({"sampling_event_device":sampling_event_device})

            if upload_session_form.is_valid():
                upload_session = upload_session_form.save(commit=False)
                upload_session.created_by = self.request.user
                upload_session.save()

                return HttpResponse(json.dumps({"upload_session_pk":upload_session.pk}), content_type="application/json")

        elif 'success_pks' in self.request.GET:
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

    def handle_finish_create(self,new_object=None):
        #next_url = self.request.GET.get('next', None)
        chain_str, next_url = self.get_new_chain()

        if next_url == '':
            return redirect(self.get_success_url())

        redirect_url = next_url+"?&chain="+chain_str+"&created_object=multiple"

        return redirect(redirect_url)

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

                    return HttpResponse(
                        json.dumps(error_data),
                        content_type="application/json",
                        status=400)

            if 'async' in self.request.GET:
                success_data = {
                    'success_pk': item.pk
                }
                return HttpResponse(
                    json.dumps(success_data),
                    content_type="application/json")

            return self.handle_finish_create(item)

        self.object = None
        context = self.get_context_data()
        context['form'] = form

        return self.render_to_response(context)
