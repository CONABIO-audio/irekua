# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from database.models import UserData, User, Institution


class UserDataSerializer(serializers.ModelSerializer):
    institution_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:institution-detail',
        source='institution')
    institution = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=Institution.objects.all(),
        slug_field='institution_code',
        allow_null=True)

    class Meta:
        model = UserData
        fields = (
            'institution',
            'institution_url',
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    userdata = UserDataSerializer(
        many=False,
        read_only=False,
        required=False)

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'userdata',
        )
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        userdata = validated_data.pop('userdata', {})
        user = User.objects.create(**validated_data)
        userdata['user'] = user
        UserData.objects.create(**userdata)
        return user

    def update(self, instance, validated_data):
        userdata = validated_data.pop('userdata', {})

        if not hasattr(instance, 'userdata'):
            UserData.objects.create(user=instance)

        instance_userdata = instance.userdata
        institution = userdata.get('institution', None)
        if institution is not None:
            instance_userdata.institution = institution
        instance_userdata.save()

        instance.userdata = instance_userdata

        email = validated_data.get('email', None)
        if email is not None:
            instance.email = email
        first_name = validated_data.get('first_name', None)
        if first_name is not None:
            instance.first_name = first_name
        last_name = validated_data.get('last_name', None)
        if last_name is not None:
            instance.last_name = last_name

        instance.save()
        return instance


class FullUserDataSerializer(serializers.ModelSerializer):
    institution_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:institution-detail',
        source='institution')
    institution = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=Institution.objects.all(),
        slug_field='institution_code',
        allow_null=True)

    class Meta:
        model = UserData
        fields = (
            'institution',
            'institution_url',
            'is_curator',
            'is_developer',
            'is_model',
        )
        extra_kwargs = {
            'is_curator': {'read_only': True},
            'is_developer': {'read_only': True},
            'is_model': {'read_only': True},
        }


class FullUserSerializer(serializers.ModelSerializer):
    userdata = FullUserDataSerializer(
        many=False,
        read_only=False,
        required=False)

    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'userdata',
            'is_superuser',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'is_superuser': {'read_only': True}
        }

    def create(self, validated_data):
        userdata = validated_data.pop('userdata', {})
        user = User.objects.create(**validated_data)
        userdata['user'] = user
        UserData.objects.create(**userdata)
        return user

    def update(self, instance, validated_data):
        userdata = validated_data.pop('userdata', {})

        if not hasattr(instance, 'userdata'):
            UserData.objects.create(user=instance)

        instance_userdata = instance.userdata
        institution = userdata.get('institution', None)
        if institution is not None:
            instance_userdata.institution = institution
        instance_userdata.save()

        instance.userdata = instance_userdata

        email = validated_data.get('email', None)
        if email is not None:
            instance.email = email
        first_name = validated_data.get('first_name', None)
        if first_name is not None:
            instance.first_name = first_name
        last_name = validated_data.get('last_name', None)
        if last_name is not None:
            instance.last_name = last_name

        instance.save()
        return instance
