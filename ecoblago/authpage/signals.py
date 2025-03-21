# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from django.contrib.staticfiles import finders
import os

from authpage.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    user = User.objects.get(pk=instance.pk)
    if not user.image:
        default_image_path = finders.find('img/noname_user.png')
        with open(default_image_path, 'rb') as f:
            user.image.save(os.path.basename(default_image_path), File(f), save=True)
