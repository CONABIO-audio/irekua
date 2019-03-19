# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from rest_framework import serializers
from database.models.roles import RESTRICT_PERMISSIONS_TO_MODELS
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


class SelectPermissionSerializer(serializers.ModelSerializer):
    codename = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='codename',
        queryset=Permission.objects.filter(
            content_type__model__in=RESTRICT_PERMISSIONS_TO_MODELS)
        )

    class Meta:
        model = Permission
        fields = (
            'codename',
        )


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=db.Role.objects.all(),
        slug_field='name')

    class Meta:
        model = db.Role
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Role
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = db.Role
        fields = (
            'url',
            'name',
            'description',
            'permissions',
            'icon',
            'modified_on',
            'created_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Role
        fields = (
            'name',
            'description',
            'icon',
        )
