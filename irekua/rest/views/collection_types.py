# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import database.models as db
from rest.serializers.collection_types import (
    ListSerializer,
    DetailSerializer,
    CreateAndUpdateSerializer,
    SiteTypeSerializer,
    AnnotationTypeSerializer,
    ItemTypeSerializer,
    EventTypeSerializer,
    LicenceTypeSerializer,
    DeviceTypeSerializer,
    SamplingEventTypeSerializer,
    RoleSerializer,
    UserSerializer,
)
from .utils import AdditionalActions


class CollectionTypeViewSet(viewsets.ModelViewSet, AdditionalActions):
    queryset = db.CollectionType.objects.all()
    serializer_class = CreateAndUpdateSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ListSerializer
        if self.action == 'retrieve':
            return DetailSerializer
        return super(CollectionTypeViewSet, self).get_serializer_class()

    @action(
        detail=True,
        methods=['GET'],
        url_name='annotationtypes',
        serializer_class=AnnotationTypeSerializer)
    def annotation_types(self, request, pk=None):
        collection_type = self.get_object()
        annotation_types = collection_type.annotation_types.all()
        return self.return_related_object_list(
            request,
            annotation_types,
            AnnotationTypeSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='sitetypes',
        serializer_class=SiteTypeSerializer)
    def site_types(self, request, pk=None):
        collection_type = self.get_object()
        site_types = collection_type.site_types.all()
        return self.return_related_object_list(
            request,
            site_types,
            SiteTypeSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='devicetypes',
        serializer_class=DeviceTypeSerializer)
    def device_types(self, request, pk=None):
        collection_type = self.get_object()
        device_types = db.CollectionDeviceType.objects.filter(
            collection_type=collection_type)
        return self.return_related_object_list(
            request,
            device_types,
            DeviceTypeSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='licencetypes',
        serializer_class=LicenceTypeSerializer)
    def licence_types(self, request, pk=None):
        collection_type = self.get_object()
        licence_types = collection_type.licence_types.all()
        return self.return_related_object_list(
            request,
            licence_types,
            LicenceTypeSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='eventtypes',
        serializer_class=EventTypeSerializer)
    def event_types(self, request, pk=None):
        collection_type = self.get_object()
        event_types = collection_type.event_types.all()
        return self.return_related_object_list(
            request,
            event_types,
            EventTypeSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='itemtypes',
        serializer_class=ItemTypeSerializer)
    def item_types(self, request, pk=None):
        collection_type = self.get_object()
        item_types = db.CollectionItemType.objects.filter(
            collection_type=collection_type)
        return self.return_related_object_list(
            request,
            item_types,
            ItemTypeSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='roles',
        serializer_class=RoleSerializer)
    def roles(self, request, pk=None):
        collection_type = self.get_object()
        roles = collection_type.roles.all()
        return self.return_related_object_list(
            request,
            roles,
            RoleSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='administrators',
        serializer_class=UserSerializer)
    def administrators(self, request, pk=None):
        collection_type = self.get_object()
        administrators = collection_type.administrators.all()
        return self.return_related_object_list(
            request,
            administrators,
            UserSerializer)

    @action(
        detail=True,
        methods=['GET'],
        url_name='samplingeventtypes',
        serializer_class=SamplingEventTypeSerializer)
    def sampling_event_types(self, request, pk=None):
        collection_type = self.get_object()
        sampling_event_types = collection_type.sampling_event_types.all()
        return self.return_related_object_list(
            request,
            sampling_event_types,
            SamplingEventTypeSerializer)

    @site_types.mapping.post
    def add_site_type(self, request, pk=None):
        collection_type = self.get_object()
        site_type = self.get_related_object(
            request,
            SiteTypeSerializer,
            db.SiteType)
        collection_type.add_site_type(site_type)
        return Response(status=status.HTTP_200_OK)

    @event_types.mapping.post
    def add_event_type(self, request, pk=None):
        return self.add_related_object_view(
            request,
            db.EventType,
            'add_event_type')
        # collection_type = self.get_object()
        # event_type = self.get_related_object(
            # request,
            # EventTypeSerializer,
            # db.EventType)
        # collection_type.add_event_type(event_type)
        # return Response(status=status.HTTP_200_OK)

    @device_types.mapping.post
    def add_device_type(self, request, pk=None):
        collection_type = self.get_object()
        device_type, extra = self.get_related_object(
            request,
            DeviceTypeSerializer,
            db.DeviceType,
            extra=['metadata_schema'])
        collection_type.add_device_type(device_type, extra['metadata_schema'])
        return Response(status=status.HTTP_200_OK)

    @licence_types.mapping.post
    def add_licence_type(self, request, pk=None):
        collection_type = self.get_object()
        licence_type = self.get_related_object(
            request,
            LicenceTypeSerializer,
            db.LicenceType)
        collection_type.add_licence_type(licence_type)
        return Response(status=status.HTTP_200_OK)

    @item_types.mapping.post
    def add_item_type(self, request, pk=None):
        collection_type = self.get_object()
        item_type, extra = self.get_related_object(
            request,
            ItemTypeSerializer,
            db.ItemType,
            extra=['metadata_schema'])
        collection_type.add_item_type(
            item_type,
            extra['metadata_schema'])
        return Response(status=status.HTTP_200_OK)

    @annotation_types.mapping.post
    def add_annotation_type(self, request, pk=None):
        collection_type = self.get_object()
        annotation_type = self.get_related_object(
            request,
            AnnotationTypeSerializer,
            db.AnnotationType)
        collection_type.add_annotation_type(annotation_type)
        return Response(status=status.HTTP_200_OK)

    @sampling_event_types.mapping.post
    def add_sampling_event_type(self, request, pk=None):
        collection_type = self.get_object()
        sampling_event_type = self.get_related_object(
            request,
            SamplingEventTypeSerializer,
            db.SamplingEventType)
        collection_type.add_sampling_event_type(sampling_event_type)
        return Response(status=status.HTTP_200_OK)

    @roles.mapping.post
    def add_role(self, request, pk=None):
        collection_type = self.get_object()
        role = self.get_related_object(
            request,
            RoleSerializer,
            db.Role)
        collection_type.add_role(role)
        return Response(status=status.HTTP_200_OK)

    @administrators.mapping.post
    def add_administrator(self, request, pk=None):
        collection_type = self.get_object()
        user = self.get_related_object(
            request,
            UserSerializer,
            db.User)
        collection_type.add_administrator(user)
        return Response(status=status.HTTP_200_OK)

    @administrators.mapping.delete
    def remove_administrator(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.administrators)
        for user in queryset:
            collection_type.remove_administrator(user)
        return Response(status=status.HTTP_200_OK)

    @site_types.mapping.delete
    def remove_site_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.site_types)
        for site_type in queryset:
            collection_type.remove_site_type(site_type)
        return Response(status=status.HTTP_200_OK)

    @roles.mapping.delete
    def remove_role(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.roles)
        for role in queryset:
            collection_type.remove_role(role)
        return Response(status=status.HTTP_200_OK)

    @sampling_event_types.mapping.delete
    def remove_sampling_event_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.sampling_event_types)
        for sampling_event_type in queryset:
            collection_type.remove_sampling_event_type(sampling_event_type)
        return Response(status=status.HTTP_200_OK)

    @event_types.mapping.delete
    def remove_event_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.event_types)
        for event_type in queryset:
            collection_type.remove_event_type(event_type)
        return Response(status=status.HTTP_200_OK)

    @device_types.mapping.delete
    def remove_device_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.device_types)
        for device_type in queryset:
            collection_type.remove_device_type(device_type)
        return Response(status=status.HTTP_200_OK)

    @licence_types.mapping.delete
    def remove_licence_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.licence_types)
        for licence_type in queryset:
            collection_type.remove_licence_type(licence_type)
        return Response(status=status.HTTP_200_OK)

    @item_types.mapping.delete
    def remove_item_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.item_types)
        for item_type in queryset:
            collection_type.remove_item_type(item_type)
        return Response(status=status.HTTP_200_OK)

    @annotation_types.mapping.delete
    def remove_annotation_type(self, request, pk=None):
        collection_type = self.get_object()
        queryset = self.filter_related_queryset(
            request,
            collection_type.annotation_types)
        for annotation_type in queryset:
            collection_type.remove_annotation_type(annotation_type)
        return Response(status=status.HTTP_200_OK)
