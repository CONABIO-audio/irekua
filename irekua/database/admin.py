from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
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
    models.Model,
    models.Synonym,
    models.Schema,
    models.CollectionSchema)
class AuthorAdmin(admin.ModelAdmin):
    pass


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = models.UserData
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
