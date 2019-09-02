from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

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

class ComplexTermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)
    entailments = EntailmentSerializer(
        many=True,
        read_only=True,
        source='entailment_source')

    class Meta:
        model = models.Term
        fields = [
            'term_type',
            'value',
            'description',
            'entailments'
        ]


class SynonymSerializer(serializers.ModelSerializer):
    source = TermSerializer()
    target = ComplexTermSerializer()

    class Meta:
        model = models.Term
        fields = [
            'source',
            'target',
        ]


class TermListView(APIView):
    rows = 7

    def get_term_queryset(self):
        name = self.request.GET['name']
        term_type = self.request.GET.get('term_type', '')

        if term_type:
            queryset = models.Term.objects.filter(
                value__icontains=name,
                term_type__name=term_type)
        else:
            queryset = models.Term.objects.filter(
                value__icontains=name)

        rows = self.request.GET.get('rows', self.rows)
        return queryset[:rows]

    def get_synonym_queryset(self):
        name = self.request.GET['name']
        term_type = self.request.GET.get('term_type', '')

        if term_type:
            queryset = models.Synonym.objects.filter(
                source__value__icontains=name,
                source__term_type__name=term_type)
        else:
            queryset = models.Synonym.objects.filter(
                source__value__icontains=name)

        rows = self.request.GET.get('rows', self.rows)
        return queryset[:rows]

    def get(self, request, format=None):
        term_queryset = self.get_term_queryset()
        synonym_queryset = self.get_synonym_queryset()

        term_serializer = ComplexTermSerializer(
            term_queryset,
            many=True)
        synonym_serializer = SynonymSerializer(
            synonym_queryset,
            many=True)

        query_results = {
            'terms': term_serializer.data,
            'synonyms': synonym_serializer.data
        }

        return Response(query_results)
