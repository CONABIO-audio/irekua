from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    institution = models.ForeignKey(
        'Institution',
        on_delete=models.PROTECT,
        db_column='institution_id',
        verbose_name=_('institution'),
        help_text=_('Institution to which user belongs'),
        blank=True,
        null=True)
    is_developer = models.BooleanField(
        db_column='is_developer',
        verbose_name=_('is developer'),
        help_text=_('Flag to indicate if user is a model developer'),
        blank=False,
        null=False,
        default=False)
    is_curator = models.BooleanField(
        db_column='is_curator',
        verbose_name=_('is curator'),
        help_text=_('Flag to indicate if user is a curator'),
        blank=False,
        null=False,
        default=False)
    is_model = models.BooleanField(
        db_column='is_model',
        verbose_name=_('is model'),
        help_text=_('Flag to indicate if user is an AI model'),
        blank=False,
        null=False,
        default=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
