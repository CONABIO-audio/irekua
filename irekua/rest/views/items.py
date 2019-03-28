# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import Permission
import django_filters

import database.models as db
from rest.serializers import items
from rest.filters import BaseFilter
from .utils import NoCreateViewSet


class Filter(BaseFilter):
    is_uploaded = django_filters.BooleanFilter(
        field_name='item_file',
        method='is_uploaded_filter',
        label='is uploaded')

    def is_uploaded_filter(self, queryset, name, value):
        return queryset.filter(item_file__isnull=False)

    class Meta:
        model = db.Item
        fields = (
            'is_uploaded',
            'item_type__name',
            'sampling_event__sampling_event_type__name',
            'sampling_event__collection__name',
            'sampling_event__collection__collection_type',
            'sampling_event__site__site_type__name',
            'sampling_event__device__device__device_type__name',
            'sampling_event__device__device__brand__name',
        )


class ItemViewSet(NoCreateViewSet):
    serializer_module = items
    filterset_class = Filter
    search_fields = ('item_type__name', )

    def get_queryset(self):
        user = self.request.user

        is_special_user = (
            user.is_superuser |
            user.is_curator |
            user.is_model |
            user.is_developer
        )
        if is_special_user:
            return self.get_full_queryset()

        return self.get_normal_queryset(user)

    def get_normal_queryset(self, user):
        is_open = (
            Q(licence__is_active=False) |
            Q(licence__licence_type__can_view=True)
        )
        is_owner = Q(sampling_event__created_by=user.pk)

        perm = Permission.objects.get(codename='view_collection_items')
        collections_with_permission = (
            db.CollectionUser.filter(
                user=user.pk,
                role__in=perm.role_set.all()
            ).select_related('collection')
        )

        is_in_allowed_collection = Q(
            sampling_event__collection__in=collections_with_permission)

        filter_query = (
            is_open |
            is_owner |
            is_in_allowed_collection
        )

        queryset = db.Item.objects.filter(filter_query)
        return queryset

    def get_full_queryset(self):
        return db.Item.objects.all()



class CollectionItemViewSet(NoCreateViewSet):
    serializer_module = items

    def get_queryset(self):
        try:
            user = self.request.user
            collection_pk = self.kwargs['collection_pk']
            collection_user = db.CollectionUser.objects.get(
                collection=collection_pk,
                user=user.pk)
            return self.get_queryset_for_collection_user(collection_user)

        except db.CollectionUser.DoesNotExist:
            return self.get_queryset_for_outsider_user()

    def get_queryset_for_outsider_user(self):
        collection_pk = self.kwargs['collection_pk']
        is_open = (
            Q(licence__is_active=False) |
            Q(licence__licence_type__can_view=True))
        is_in_collection = Q(sampling_event__collection=collection_pk)
        return db.Item.objects.filter(is_open & is_in_collection)

    def get_queryset_for_collection_user(self, collection_user):
        user = collection_user.user
        role = collection_user.role

        if collection_user.is_admin | user.is_superuser:
            return self.get_full_queryset()

        if 'database.view_collection_items' in role.permissions.all():
            return self.get_full_queryset()

        return self.get_queryset_for_collection_user_without_perms(user)

    def get_full_queryset(self):
        collection_pk = self.kwargs['collection_pk']
        return db.Item.objects.filter(sampling_event__collection=collection_pk)

    def get_queryset_for_collection_user_without_perms(self, user):
        collection_pk = self.kwargs['collection_pk']
        is_open = (
            Q(licence__is_active=False) |
            Q(licence__licence_type__can_view=True))
        is_in_collection = Q(sampling_event__collection=collection_pk)
        is_owner = Q(sampling_event__created_by=user.pk)
        return db.Item.objects.filter((is_owner | is_open) & is_in_collection)
