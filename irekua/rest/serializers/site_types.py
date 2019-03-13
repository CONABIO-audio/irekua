# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SiteTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema'
        )
