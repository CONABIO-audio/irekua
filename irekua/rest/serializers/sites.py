# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Site
        fields = (
            'url',
            'name',
            'geo_ref',
            'latitude',
            'longitude',
            'altitude',
            'metadata_type',
            'metadata',
            'creator')
