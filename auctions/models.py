from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    image = models.URLField(null=True,max_length=400)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.image} {self.description} {self.price} {self.date}"