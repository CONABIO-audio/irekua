from django.contrib import admin
from . import models


# Register your models here.
@admin.register(
    models.Annotation,
    models.Term,
    models.Collection,
    models.CollectionOwner,
    models.Device,
    models.Entailment,
    models.Item,
    models.Licence,
    models.SamplingEvent,
    models.SecondaryItem,
    models.Site,
    models.Source,
    models.UserData,
    models.Model,
    models.Synonym)
class AuthorAdmin(admin.ModelAdmin):
    pass
