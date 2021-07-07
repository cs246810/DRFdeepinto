from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    tel = models.CharField(max_length=255, unique=True, null=False)
    headshot = models.ImageField(default=settings.DEFAULT_USER_HEADSHOT)
    address = models.CharField(max_length=1024, null=False)

    class Meta:
        ordering = ['-date_joined']

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    parent = models.IntegerField(default=0)
    headshot = models.ImageField(default=settings.DEFAULT_CATEGORY_HEADSHOT)

    def __str__(self): return self.name

    class Meta:
        ordering = ['id']

class Goods(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    unit_price = models.FloatField(null=False)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    headshot = models.ImageField(default=settings.DEFAULT_GOODS_HEADSHOT)

    def __str__(self): return self.name

    class Meta: ordering = ['id']

class GoodsImage(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.ImageField()
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['goods', 'title', 'category']]
        ordering = ['id']

class GoodsVideo(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.FileField()
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['goods', 'title', 'category']]
        ordering = ['id']