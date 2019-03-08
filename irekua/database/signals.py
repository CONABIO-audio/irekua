from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver


@receiver(pre_save)
def validate_model(sender, instance, raw=False, **kwargs):
    if not isinstance(sender, models.Model):
        return

    if not raw:
        instance.full_clean()
