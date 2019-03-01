from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserData(models.Model):
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
        verbose_name = _('User Data')
        verbose_name_plural = _('Users Data')

    def __str__(self):
        return str(self.user)
