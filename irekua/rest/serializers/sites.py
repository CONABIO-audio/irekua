# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    site_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='site_type-detail')
    creator = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = db.Site
        fields = (
            'url',
            'name',
            'locality',
            'site_type',
            'geo_ref',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
            'creator'
        )
