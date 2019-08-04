from .create_base import SeliaCreateView
from database.models import Item
from database.models import Annotation
from database.models import Term
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django import forms
import urllib
import json
import requests 

class CreateTermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ["term_type","value","description","metadata"]

class CreateAnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ["annotation_tool","item","event_type","label","annotation_type","annotation","annotation_configuration","certainty","quality","commentaries"]   

class SeliaAnnotationView(SeliaCreateView):

    def proxy_to_slr(self):
        server = "snmb.conabio.gob.mx"
        slr_path = '/solr/taxonomia/select'

        query = self.request.GET.copy()
        del query['slr_service']

        url = 'http://{}{}?{}'.format(server,slr_path,query.urlencode())

        def convert(s):
            s = s.replace('HTTP_','',1)
            s = s.replace('_','-')
            return s

        request_headers = dict((convert(k),v) for k,v in self.request.META.items() if k.startswith('HTTP_'))
        request_headers['CONTENT-TYPE'] = self.request.META.get('CONTENT_TYPE', '')
        request_headers['CONTENT-LENGTH'] = self.request.META.get('CONTENT_LENGTH', '')
        request_headers['USER-AGENT'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

        if self.request.method == "GET":
            data = None
        else:
            data = self.request.raw_post_data

        req = requests.get(url = url)

        response = HttpResponse(req.text)

        return response

    def get(self, *args, **kwargs):
        if "slr_service" in self.request.GET:
            return self.proxy_to_slr()

        if "mode" in self.request.GET:
            if self.request.GET["mode"] == "edit":
                self.template_name = 'selia/item_detail/annotations/edit.html'
                self.mode = "edit"

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if "mode" in self.request.GET:
            if self.request.GET["mode"] == "edit":
                self.template_name = 'selia/item_detail/annotations/edit.html'
                self.mode = "edit"

        return super().post(*args, **kwargs)

    def get_success_url_args(self):
        return [self.kwargs['pk']]
        
    def handle_create(self):
        if self.mode == "create":
            form = self.get_form()
            label = json.loads(form.data["label"])
            label_keys = list(label.keys())

            if not Term.objects.filter(term_type=label_keys[0], value=label[label_keys[0]]).exists():
                print("CREATE!!!")
                term_form = CreateTermForm({"term_type":label_keys[0],"value":label[label_keys[0]]})
                if term_form.is_valid():
                    term = term_form.save(commit=False)
                    term.created_by = self.request.user
                    term.save()

            if form.is_valid():
                annotation = form.save(commit=False)
                annotation.created_by = self.request.user
                annotation.save()
                return self.handle_finish_create(annotation)
            else:
                print(form.errors)
                self.object = None
                context = self.get_context_data()
                context['form'] = form

                return self.render_to_response(context)
        else:
            instance = get_object_or_404(Annotation, pk=self.request.GET["annotation"])
            form = CreateAnnotationForm(self.request.POST or None, instance=instance)

            if form.is_valid():
                annotation = form.save(commit=False)
                annotation.save()
                return self.handle_finish_create(annotation)
            else:
                print(form.errors)
                self.object = None
                context = self.get_context_data()
                context['form'] = form

                return self.render_to_response(context)              

    def get_initial(self):
        item = Item.objects.get(pk=self.kwargs['pk'])
        initial = {
            'item': item
        }

        return initial

    def get_annotation_list(self):
        queryset = Annotation.objects.filter(item__pk=self.kwargs['pk'])
        return queryset

    def get_annotator_template(self):
        if hasattr(self, 'annotator_template'):
            return self.annotator_template

        raise NotImplementedError('No template for annotator was given')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mode'] = self.mode
        context['item'] = self.get_object(queryset=Item.objects.all())
        context["annotation_list"] = self.get_annotation_list()
        context['annotator_template'] = self.get_annotator_template()

        if self.mode == "edit":
            instance = get_object_or_404(Annotation, pk=self.request.GET["annotation"])
            form = CreateAnnotationForm(instance=instance)
            context["form"] = form
            context["annotation"] = instance

        return context


