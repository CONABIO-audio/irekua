from django.db import models

from .data_collections import Collection
from .schemas import Schema


class CollectionSchema(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE)
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE)
