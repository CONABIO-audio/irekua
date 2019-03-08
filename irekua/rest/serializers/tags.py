# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Tag
        fields = (
                'url',
                )
