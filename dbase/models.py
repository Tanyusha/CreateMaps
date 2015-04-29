from django.db import models


class DBase(models.Model):
    name = models.CharField(max_length=200)
