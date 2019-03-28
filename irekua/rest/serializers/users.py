# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import User
from . import institutions


class SelectSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=User.objects.all())

    class Meta:
        model = User
        fields = (
            'url',
            'username',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    institution = institutions.ListSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'institution'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    institution = institutions.DetailSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'first_name',
            'last_name',
            'institution',
        )


class FullDetailSerializer(serializers.HyperlinkedModelSerializer):
    institution = institutions.DetailSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'institution',
            'last_login',
            'date_joined',
            'is_superuser',
            'is_curator',
            'is_developer',
            'is_model',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'institution',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'institution',
        )
