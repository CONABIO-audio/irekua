# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import EntailmentTypeSerializer
from rest.permissions import IsAdmin, ReadOnly, IsDeveloper


class EntailmentTypeViewSet(ModelViewSet):
    queryset = db.EntailmentType.objects.all()
    serializer_class = EntailmentTypeSerializer
    permission_classes = (IsAdmin|IsDeveloper|ReadOnly, )
    search_fields = ('source_type__name', 'target_type__name')
    filter_fields = ('source_type__name', 'target_type__name')
