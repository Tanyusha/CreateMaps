from customauth.models import MyUser
from django.db import models

# from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

POINT = 1
POLYGON = 2
TYPES = (
    (POINT, "point"),
    (POLYGON, "polygon"),
)


class Map(models.Model):
    user = models.ForeignKey(MyUser, related_name='ownable_maps')
    editors = models.ManyToManyField(MyUser, related_name='editable_maps', blank=True)
    name = models.CharField(max_length=512)
    description = models.TextField()

    class Meta:
        verbose_name = u'карта'
        verbose_name_plural = u'карты'


class Dataset(models.Model):
    map = models.ForeignKey(Map)
    name = models.CharField(max_length=512)


class MObject(models.Model):
    map = models.ForeignKey(Map)
    dataset = models.ForeignKey(Dataset)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    # geom = models.MultiPolygonField(srid=4326)
    type = models.IntegerField(choices=TYPES, default=POINT)
    data = HStoreField()


class Point(models.Model):
    object = models.ForeignKey(MObject)
    lon = models.FloatField()
    lat = models.FloatField()


class Field(models.Model):
    map = models.ForeignKey(Map)
    name = models.CharField(max_length=512)
    is_required = models.BooleanField(default=False)
    is_filter = models.BooleanField(default=False)
