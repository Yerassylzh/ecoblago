from django.db.models.signals import pre_delete
from django.dispatch import receiver
from catalog.models import GalleryImage

@receiver(pre_delete, sender=GalleryImage)
def delete_gallery_image_file(sender, instance, **kwargs):
    if instance.image:
        storage = instance.image.storage
        if storage.exists(instance.image.name):
            storage.delete(instance.image.name)
