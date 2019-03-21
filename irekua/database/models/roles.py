from django.db import models
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _


RESTRICT_PERMISSIONS_TO_MODELS = [
    'collection',
    'item',
    'annotation',
]


class Role(models.Model):
    name = models.CharField(
        max_length=64,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of role'),
        blank=False,
        null=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of role'),
        blank=True)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Role type icon'),
        upload_to='images/role_types/',
        blank=True,
        null=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        help_text=_('Permissions associated to role'),
        limit_choices_to=models.Q(content_type__model='collection'),
        blank=True)

    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of entry creation'),
        auto_now_add=True,
        editable=False)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        auto_now=True,
        editable=False)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

        ordering = ['name']

    def __str__(self):
        return self.name

    def add_permission(self, permission):
        self.permissions.add(permission)
        self.save()

    def remove_permission(self, permission):
        self.permissions.remove(permission)
        self.save()
