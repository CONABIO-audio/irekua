# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionSiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionSite
        fields = (
            'url',
            'site',
            'collection',
            'internal_id',
            'metadata_type',
            'metadata',
        )
