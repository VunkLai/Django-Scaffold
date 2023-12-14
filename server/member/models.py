from django.contrib.auth import get_user_model
from django.db import models

Member = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
