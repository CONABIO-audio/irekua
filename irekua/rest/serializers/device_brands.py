# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class DeviceBrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceBrand
        fields = (
            'url',
            'name',
            'website',
            'logo',
        )
