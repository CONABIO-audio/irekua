# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class LicenceTypeSerializer(serializers.HyperlinkedModelSerializer):
    metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')

    class Meta:
        model = db.LicenceType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )
