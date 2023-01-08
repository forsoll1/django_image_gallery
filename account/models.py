from django.db import models

from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_slideshow = models.BooleanField()

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance, show_slideshow = True)
        instance.settings.save()