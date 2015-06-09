from django.db import models

# from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

POINT = 1
POLYGON = 2
TYPES = (
    (POINT, "point"),
    (POLYGON, "polygon"),
)


class Filter(models.Model):
    name = models.CharField(max_length=512)


class Dataset(models.Model):
    name = models.CharField(max_length=512)


class MObject(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    # geom = models.MultiPolygonField(srid=4326)
    dataset = models.ForeignKey(Dataset)
    type = models.IntegerField(choices=TYPES, default=POINT)
    data = HStoreField()


class Map(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    filters = models.ManyToManyField(Filter)
    datasets = models.ManyToManyField(Dataset)


class Points(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    Objects = models.ManyToManyField(MObject)