from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField(default=0)
