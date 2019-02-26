from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleType(models.Model):
    name = models.CharField(
        max_length=16,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of role'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of role'),
        blank=True)

    can_add_items = models.BooleanField(
        db_column='can_add_items',
        verbose_name=_('can add items'),
        help_text=_('Can add items to collection'),
        blank=False,
        null=False)
    can_view_items = models.BooleanField(
        db_column='can_view_items',
        verbose_name=_('can view items'),
        help_text=_('Can view items in collection'),
        blank=False,
        null=False)
    can_update_items = models.BooleanField(
        db_column='can_update_items',
        verbose_name=_('can update items'),
        help_text=_('Can update items in collection'),
        blank=False,
        null=False)
    can_download_items = models.BooleanField(
        db_column='can_download_items',
        verbose_name=_('can download items'),
        help_text=_('Can download items in collection'),
        blank=False,
        null=False)

    can_add_sites = models.BooleanField(
        db_column='can_add_sites',
        verbose_name=_('can add sites'),
        help_text=_('Can add sites to collection'),
        blank=False,
        null=False)
    can_view_sites = models.BooleanField(
        db_column='can_view_sites',
        verbose_name=_('can view sites'),
        help_text=_('Can view sites in collection'),
        blank=False,
        null=False)
    can_update_sites = models.BooleanField(
        db_column='can_update_sites',
        verbose_name=_('can update sites'),
        help_text=_('Can update sites in collection'),
        blank=False,
        null=False)
    can_remove_sites = models.BooleanField(
        db_column='can_remove_sites',
        verbose_name=_('can remove sites'),
        help_text=_('Can remove sites from collection'),
        blank=False,
        null=False)

    can_add_devices = models.BooleanField(
        db_column='can_add_devices',
        verbose_name=_('can add devices'),
        help_text=_('Can add devices to collection'),
        blank=False,
        null=False)
    can_view_devices = models.BooleanField(
        db_column='can_view_devices',
        verbose_name=_('can view devices'),
        help_text=_('Can view devices in collection'),
        blank=False,
        null=False)
    can_update_devices = models.BooleanField(
        db_column='can_update_devices',
        verbose_name=_('can update devices'),
        help_text=_('Can update devices in collection'),
        blank=False,
        null=False)
    can_remove_devices = models.BooleanField(
        db_column='can_remove_devices',
        verbose_name=_('can remove devices'),
        help_text=_('Can remove devices from collection'),
        blank=False,
        null=False)

    can_add_schemas = models.BooleanField(
        db_column='can_add_schemas',
        verbose_name=_('can add schemas'),
        help_text=_('Can add schemas to collection'),
        blank=False,
        null=False)
    can_remove_schemas = models.BooleanField(
        db_column='can_remove_schemas',
        verbose_name=_('can remove schemas'),
        help_text=_('Can remove schemas from collection'),
        blank=False,
        null=False)

    can_add_roles = models.BooleanField(
        db_column='can_add_roles',
        verbose_name=_('can add roles'),
        help_text=_('Can add roles to collection'),
        blank=False,
        null=False)
    can_remove_roles = models.BooleanField(
        db_column='can_remove_roles',
        verbose_name=_('can remove roles'),
        help_text=_('Can remove roles from collection'),
        blank=False,
        null=False)

    can_add_users = models.BooleanField(
        db_column='can_add_users',
        verbose_name=_('can add users'),
        help_text=_('Can add users to collection'),
        blank=False,
        null=False)
    can_update_users = models.BooleanField(
        db_column='can_update_users',
        verbose_name=_('can update users'),
        help_text=_('Can update users in collection'),
        blank=False,
        null=False)
    can_remove_users = models.BooleanField(
        db_column='can_remove_users',
        verbose_name=_('can remove users'),
        help_text=_('Can remove users from collection'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Role Type')
        verbose_name_plural = _('Role Types')

    def __str__(self):
        return self.name
