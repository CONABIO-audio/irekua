from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django_filters import FilterSet

from database import models


class EntailmentSerializer(serializers.Serializer):
    term_type = serializers.CharField(
        source='target.term_type')
    description = serializers.CharField(
        source='target.description')
    value = serializers.CharField(
        source='target.value')


class TermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Term
        fields = [
            'term_type',
            'value',
            'description',
        ]


class SynonymSerializer(serializers.ModelSerializer):
    target = TermSerializer()

    class Meta:
        model = models.Term
        fields = [
            'target',
        ]


class ComplexTermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)
    entailments = EntailmentSerializer(
        many=True,
        read_only=True,
        source='entailment_source')
    synonyms = SynonymSerializer(
        many=True,
        source='synonym_source')

    class Meta:
        model = models.Term
        fields = [
            'term_type',
            'value',
            'description',
            'entailments',
            'synonyms',
        ]


class TermFilter(FilterSet):
    class Meta:
        model = models.Term
        fields = {
            'value': ['icontains'],
            'term_type': ['exact']
        }


class TermListView(GenericAPIView):
    rows = 7
    serializer_class = ComplexTermSerializer
    filterset_class = TermFilter
    queryset = models.Term.objects.all()

    def get(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
