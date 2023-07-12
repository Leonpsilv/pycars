from django.db import models

from users.models import User


class AvatarModel(models.Model):
    url = models.CharField(blank=False, default="")
    filename = models.CharField(blank=False, default="")
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.OneToOneField(
        User, related_name="avatar", on_delete=models.CASCADE
    )
