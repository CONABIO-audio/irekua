from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models


# Register your models here.
@admin.register(
    models.Annotation,
    models.AnnotationTool,
    models.AnnotationType,
    models.AnnotationVote,
    models.Collection,
    models.CollectionDevice,
    models.CollectionDeviceType,
    models.CollectionItemType,
    models.CollectionRole,
    models.CollectionSite,
    models.CollectionType,
    models.CollectionLicence,
    models.CollectionUser,
    models.Device,
    models.DeviceBrand,
    models.DeviceType,
    models.Entailment,
    models.EntailmentType,
    models.EventType,
    models.Institution,
    models.Item,
    models.ItemType,
    models.Licence,
    models.LicenceType,
    models.MetaCollection,
    models.PhysicalDevice,
    models.Role,
    models.SamplingEvent,
    models.SamplingEventType,
    models.SecondaryItem,
    models.Site,
    models.SiteType,
    models.Source,
    models.Synonym,
    models.SynonymSuggestion,
    models.Tag,
    models.Term,
    models.TermSuggestion,
    models.TermType,
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
