from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    steam_id = models.CharField(max_length=20, blank=True, null=True)
