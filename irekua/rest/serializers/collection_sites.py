# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionSiteSerializer(serializers.HyperlinkedModelSerializer):
    site = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='site-detail')
    collection = serializers.HyperlinkedRelatedField(
            many=False,
            read_only=True,
            view_name='collection-detail')

    class Meta:
        model = db.CollectionSite
        fields = (
            'url',
            'site',
            'collection',
            'internal_id',
            'metadata',
        )
