from django.db import models
from dal import autocomplete
from database import models as irekua_models


class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Institution.objects.all()

        if self.q:
            institution_name_query = models.Q(institution_name__istartswith=self.q)
            institution_code_query = models.Q(institution_code__istartswith=self.q)
            qs = qs.filter(institution_name_query | institution_code_query)

        return qs


class DeviceBrandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.DeviceBrand.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class DeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Device.objects.all()

        if self.q:
            brand_query = models.Q(brand__name__istartswith=self.q)
            model_query = models.Q(model__istartswith=self.q)
            qs = qs.filter(brand_query | model_query)

        return qs


class CollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Collection.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class MetacollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.MetaCollection.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TermsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Collection.objects.all()

        term_type = self.forwarded.get('term_type', None)

        if term_type:
            qs = qs.filter(term_type=term_type)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class AnnotationToolsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = irekua_models.AnnotationTool.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
