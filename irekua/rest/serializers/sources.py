# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Source
        fields = (
            'url',
            'directory',
            'source_file',
            'parse_function',
            'uploaded_on',
            'uploader',
        )
