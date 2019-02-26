# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Item
        fields = (
            'url',
            'type',
            'media_info',
            'metadata',
            'keywords',
            'captured_on',
            'sampling',
            'collection',
            'owner',
            'licence')
