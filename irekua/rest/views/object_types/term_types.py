# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from database.models import TermType
from database.models import TermSuggestion
from database.models import Synonym
from database.models import SynonymSuggestion
from database.models import Entailment
from database.models import EntailmentType

from rest.serializers.object_types import term_types
from rest.serializers.object_types import entailment_types as entailment_type_serializers
from rest.serializers.terms import term_suggestions
from rest.serializers.terms import synonym_suggestions as synonym_suggestion_serializers
from rest.serializers.terms import entailments as entailment_serializers
from rest.serializers.terms import synonyms as synonym_serializers
from rest.serializers.terms import terms as term_serializers

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated

from rest.filters import TermTypeFilter

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class TermTypeViewSet(CustomViewSetMixin, ModelViewSet):
    queryset = TermType.objects.all()
    search_fields = ('name', )
    filterset_class = TermTypeFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(term_types)
        .extend(
            terms=term_serializers.ListSerializer,
            add_term=term_serializers.CreateSerializer,
            suggestions=term_suggestions.ListSerializer,
            suggest_term=term_suggestions.CreateSerializer,
            entailment_types=entailment_type_serializers.ListSerializer,
            add_entailment_type=entailment_type_serializers.CreateSerializer,
            entailments=entailment_serializers.ListSerializer,
            add_entailment=entailment_serializers.CreateSerializer,
            synonyms=synonym_serializers.ListSerializer,
            add_synonym=synonym_serializers.CreateSerializer,
            synonym_suggestions=synonym_suggestion_serializers.ListSerializer,
            suggest_synonym=synonym_suggestion_serializers.CreateSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated, IsAdmin],
        Actions.CREATE: [IsAuthenticated, IsAdmin],
        Actions.UPDATE: [IsAuthenticated, IsAdmin],
        'add_term': [IsAuthenticated, IsAdmin],
        'add_entailment_type': [IsAuthenticated, IsAdmin],
        'add_entailment': [IsAuthenticated, IsAdmin],
        'add_synonym': [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            term_type = self.get_object()
        except (AssertionError, AttributeError):
            term_type = None

        context['term_type'] = term_type
        return context

    @action(detail=False, methods=['GET'])
    def entailments(self, request):
        queryset = Entailment.objects.all()
        return self.list_related_object_view(queryset)

    @entailments.mapping.post
    def add_entailment(self, request):
        self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def entailment_types(self, request):
        queryset = EntailmentType.objects.all()
        return self.list_related_object_view(queryset)

    @entailment_types.mapping.post
    def add_entailment_type(self, request):
        self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def terms(self, request, pk=None):
        term_type = self.get_object()
        queryset = term_type.term_set.all()
        return self.list_related_object_view(queryset)

    @terms.mapping.post
    def add_term(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def synonyms(self, request, pk=None):
        type_id = self.kwargs['pk']
        queryset = Synonym.objects.filter(source__term_type=type_id)
        return self.list_related_object_view(queryset)

    @synonyms.mapping.post
    def add_synonym(self, request, pk=None):
        self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def suggestions(self, request, pk=None):
        type_id = self.kwargs['pk']
        queryset = TermSuggestion.objects.filter(term_type=type_id)
        return self.list_related_object_view(queryset)

    @suggestions.mapping.post
    def suggest_term(self, request, pk=None):
        self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def synonym_suggestions(self, request, pk=None):
        type_id = self.kwargs['pk']
        queryset = SynonymSuggestion.objects.filter(source__term_type=type_id)
        return self.list_related_object_view(queryset)

    @synonym_suggestions.mapping.post
    def suggest_synonym(self, request, pk=None):
        self.create_related_object_view()
