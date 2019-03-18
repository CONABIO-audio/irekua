# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class LabelTermSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.TermType.objects.all())

    class Meta:
        model = db.TermType
        fields = ('url', 'name')


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    label_term_types = LabelTermSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'label_term_types')
