# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class LicenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Licence
        fields = (
            'url',
            'licence_type',
            'document',
            'created_on',
            'valid_until',
            'metadata',
        )
