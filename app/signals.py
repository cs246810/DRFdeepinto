from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from .models import User, Category, Goods, GoodsVideo, GoodsImage
from django.conf import settings

@receiver(pre_delete, sender=models.Model)
def pre_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    if isinstance(instance, (User, Category, Goods)):
        if instance.headshot.name not in [settings.DEFAULT_USER_HEADSHOT,
                                          settings.DEFAULT_CATEGORY_HEADSHOT,
                                          settings.DEFAULT_GOODS_HEADSHOT]:
            instance.headshot.delete(True)
    elif isinstance(instance, (GoodsImage, GoodsVideo)):
        instance.file_name.delete(True)

def register_signals():
    pre_delete.connect(pre_delete_handler, sender=User)
    pre_delete.connect(pre_delete_handler, sender=Category)
    pre_delete.connect(pre_delete_handler, sender=Goods)
    pre_delete.connect(pre_delete_handler, sender=GoodsImage)
    pre_delete.connect(pre_delete_handler, sender=GoodsVideo)