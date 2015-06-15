from attrs.models import set_obj_attrs, get_obj_attrs, Attribute
from customauth.models import MyUser
from django.db import models
# from django.contrib.gis.db import models
# from django.contrib.postgres.fields import HStoreField

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
    map = models.ForeignKey(Map, related_name='datasets')
    name = models.CharField(max_length=512)


class MObject(models.Model):
    map = models.ForeignKey(Map, related_name='mobjects')
    dataset = models.ForeignKey(Dataset, related_name='mobjects')
    type = models.IntegerField(choices=TYPES, default=POINT)

    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    # points = ...

    # data = HStoreField()
    def _set_data(self, data):
        set_obj_attrs(self, data)

    def _get_data(self):
        return get_obj_attrs(self)

    data = property(_get_data, _set_data)

    def __str__(self):
        return '<MObject {0}>'.format(self.id)


class Point(models.Model):
    object = models.ForeignKey(MObject, related_name='points')
    lon = models.FloatField()
    lat = models.FloatField()


class Field(models.Model):
    map = models.ForeignKey(Map, related_name='fields')
    name = models.CharField(max_length=512)
    # type = models.CharField(max_length=10, choices=Attribute.DATATYPE_CHOICES)
    is_required = models.BooleanField(default=False)
    is_filter = models.BooleanField(default=False)

    def __str__(self):
        return self.name
