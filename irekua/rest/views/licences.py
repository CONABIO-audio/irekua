# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

import database.models as db
from rest.serializers import licences
from .utils import CustomViewSet



class LicenceViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     CustomViewSet):
    queryset = db.Licence.objects.all()
    serializer_module = licences
