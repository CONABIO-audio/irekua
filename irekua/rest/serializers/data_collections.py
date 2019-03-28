# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import collection_types
from . import institutions
from . import licences


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Collection
        fields = (
            'url',
            'name',
            'logo',
            'collection_type',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = collection_types.ListSerializer(
        many=False,
        read_only=False)
    institution = institutions.ListSerializer(
        many=False,
        read_only=True)
    licence_set = licences.ListSerializer(
        many=True,
        read_only=True)

    devices = serializers.HyperlinkedIdentityField(
        view_name='rest-api:collection-devices-list',
        lookup_url_kwarg='collection_pk')
    sites = serializers.HyperlinkedIdentityField(
        view_name='rest-api:collection-sites-list',
        lookup_url_kwarg='collection_pk')
    sampling_events = serializers.HyperlinkedIdentityField(
        view_name='rest-api:collection-samplingevents-list',
        lookup_url_kwarg='collection_pk')
    items = serializers.HyperlinkedIdentityField(
        view_name='rest-api:collection-items-list',
        lookup_url_kwarg='collection_pk')

    class Meta:
        model = db.Collection
        fields = (
            'url',
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'logo',
            'licence_set',
            'created_on',
            'modified_on',
            'devices',
            'sites',
            'sampling_events',
            'items',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Collection
        fields = (
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'logo',
        )


class CollectionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retrieve_collection()
        self.update_querysets()

    def retrieve_collection(self):
        try:
            self.collection = self.context['collection']
            self.user = self.context['user']
        except KeyError:
            self.collection = None
            self.user = None

    def update_querysets(self):
        pass
