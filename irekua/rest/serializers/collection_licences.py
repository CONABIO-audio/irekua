# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionLicenceSerializer(serializers.HyperlinkedModelSerializer):
    collection = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection-detail')
    licence = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='licence-detail')

    class Meta:
        model = db.CollectionLicence
        fields = (
            'url',
            'collection',
            'licence',
        )
