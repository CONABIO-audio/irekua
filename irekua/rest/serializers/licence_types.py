# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class LicenceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.LicenceType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )
