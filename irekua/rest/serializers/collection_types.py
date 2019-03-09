# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


from .site_types import SiteTypeSerializer
from .annotation_types import AnnotationTypeSerializer
from .licence_types import LicenceTypeSerializer
from .event_types import EventTypeSerializer
from .sampling_event_types import SamplingEventTypeSerializer
from .device_types import DeviceTypeSerializer
from .roles import RoleSerializer
from .item_types import ItemTypeSerializer


class CollectionTypeSerializer(serializers.HyperlinkedModelSerializer):
    site_types = SiteTypeSerializer(many=True, read_only=True)
    annotation_types = AnnotationTypeSerializer(many=True, read_only=True)
    licence_types = LicenceTypeSerializer(many=True, read_only=True,)
    event_types = EventTypeSerializer(many=True, read_only=True)
    sampling_event_types = SamplingEventTypeSerializer(many=True, read_only=True)
    item_types = ItemTypeSerializer(many=True, read_only=True)
    device_types = DeviceTypeSerializer(many=True, read_only=True)
    roles = RoleSerializer(many=True, read_only=True)

    administrators = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username')

    class Meta:
        model = db.CollectionType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'anyone_can_create',
            'administrators',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
            'site_types',
            'annotation_types',
            'licence_types',
            'event_types',
            'sampling_event_types',
            'item_types',
            'device_types',
            'roles'
        )
