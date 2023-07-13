from django.db import models

from users.models import User


class CarModel(models.Model):
    name = models.CharField(blank=False, default="", max_length=75)
    brand = models.CharField(blank=False, default="", max_length=30)
    year = models.CharField(blank=False, default="", max_length=15)
    type = models.CharField(blank=False, default="", max_length=20)
    km = models.IntegerField(blank=False, default=0)
    price = models.IntegerField(blank=False, default=0)
    color = models.CharField(blank=False, default="", max_length=20)
    new = models.BooleanField(blank=False, default=True)
    vin = models.CharField(blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        User, related_name="car", on_delete=models.CASCADE
    )
