from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models


# Register your models here.
@admin.register(
    models.Annotation,
    models.AnnotationType,
    models.AnnotationVote,
    models.Collection,
    models.CollectionDevice,
    models.CollectionRole,
    models.CollectionSchema,
    models.CollectionSite,
    models.CollectionUser,
    models.Device,
    models.DeviceType,
    models.DeviceBrand,
    models.Entailment,
    models.EventType,
    models.Institution,
    models.Item,
    models.ItemType,
    models.Licence,
    models.LicenceType,
    models.MetaCollection,
    models.PhysicalDevice,
    models.RoleType,
    models.SamplingEvent,
    models.Schema,
    models.SecondaryItem,
    models.Site,
    models.Source,
    models.Synonym,
    models.SynonymSuggestion,
    models.Term,
    models.TermType,
    models.TermSuggestion,
    models.UserData)
class AuthorAdmin(admin.ModelAdmin):
    pass


class UserInline(admin.StackedInline):
    model = models.UserData
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
