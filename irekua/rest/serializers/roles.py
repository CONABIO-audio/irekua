# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from rest_framework import serializers
import database.models as db


class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='model',
        queryset=ContentType.objects.filter(app_label='database'))

    class Meta:
        model = Permission
        fields = (
            'content_type',
            'codename'
        )

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = db.Role
        fields = (
            'url',
            'name',
            'description',
            'permissions',
            'icon',
        )
