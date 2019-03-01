from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class RoleType(Group):
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

    class Meta:
        verbose_name = _('Role Type')
        verbose_name_plural = _('Role Types')

    def __str__(self):
        return self.name
