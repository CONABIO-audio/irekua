# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Institution
        fields = (
            'url',
            'institution_name',
            'institution_code',
            'institution_id',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
        )
