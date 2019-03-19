# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import UserData, User
from . import institutions


class UserDataSerializer(serializers.ModelSerializer):
    institution = institutions.DetailSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = UserData
        fields = (
            'institution',
        )


class FullUserDataSerializer(serializers.ModelSerializer):
    institution = institutions.DetailSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = UserData
        fields = (
            'institution',
            'is_curator',
            'is_developer',
            'is_model',
        )


class CreateUserDataSerializer(serializers.ModelSerializer):
    institution = institutions.SelectSerializer(
        many=False,
        read_only=False)

    class Meta:
        model = UserData
        fields = (
            'institution',
        )


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
    institution = serializers.CharField(
        read_only=True,
        source='userdata.institution.institution_code')

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'institution'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    userdata = UserDataSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'first_name',
            'last_name',
            'userdata'
        )


class FullDetailSerializer(serializers.HyperlinkedModelSerializer):
    userdata = FullUserDataSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'userdata',
            'is_superuser',
            'last_login',
            'date_joined',
        )


class CreateSerializer(serializers.ModelSerializer):
    userdata = CreateUserDataSerializer(
        many=False,
        read_only=False,
        required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'userdata',
        )


class UpdateSerializer(serializers.ModelSerializer):
    userdata = CreateUserDataSerializer(
        many=False,
        read_only=False,
        required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'userdata',
        )
