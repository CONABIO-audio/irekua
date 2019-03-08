# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from django.contrib.auth.models import User
from database.models import UserData


class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserData
        fields = (
            'url',
            'organization',
            'metadata'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_data = UserDataSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_data')
