from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserData(models.Model):
    USER_ROLES = [
        ('admin', 'admin'),
        ('developer', 'developer'),
        ('curator', 'curator'),
        ('model', 'model'),
        ('user', 'user'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        editable=False,
        db_column='user_id',
        verbose_name=_('user id'),
        help_text=_('Reference to user'),
        blank=False)
    institution = models.ForeignKey(
        'Institution',
        on_delete=models.PROTECT,
        db_column='institution_id',
        verbose_name=_('institution id'),
        help_text=_('Institution to which user belongs'),
        blank=False)
    role = models.CharField(
        max_length=30,
        choices=USER_ROLES,
        db_column='role',
        verbose_name=_('role'),
        help_text=_('Role of user'),
        blank=False)

    class Meta:
        verbose_name = _('User Data')
        verbose_name_plural = _('Users Data')

    def __str__(self):
        return str(self.user)
