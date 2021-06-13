from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.first_name
