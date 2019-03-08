# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class LicenceSerializer(serializers.HyperlinkedModelSerializer):
    licence_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='licence-detail')

    class Meta:
        model = db.Licence
        fields = (
            'url',
            'licence_type',
            'document',
            'created_on',
            'metadata',
        )
