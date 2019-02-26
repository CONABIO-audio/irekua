# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SamplingEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SamplingEvent
        fields = (
            'device',
            'configuration',
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
            'site')
