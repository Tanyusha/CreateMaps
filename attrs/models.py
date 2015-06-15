from __future__ import unicode_literals, print_function, generators, division
from datetime import datetime, date
from warnings import warn
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils.six import text_type, integer_types
from django.utils.translation import ugettext_lazy as _

__author__ = 'pahaz'
MODEL_ATTR_FIELD_NAME = 'attrs'
USE_FILTER_DATATYPE_DETECT_HEURISTICS = True


class Attribute(models.Model):
    """
    This model stores the name and value for some object. Most of the columns
    of this model will be blank, as only one *value_* field will be used.

    >>> v = Attribute(value=1, name='some')
    >>> v.type == Attribute.TYPE_INT
    True
    >>> v.value == 1
    True
    >>> v.name == 'some'
    True
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    value_text = models.TextField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_date = models.DateTimeField(blank=True, null=True)
    value_bool = models.NullBooleanField(blank=True, null=True)

    value_object_id = models.IntegerField(blank=True, null=True)
    value_content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                           related_name='attribute_value_set')
    value_object = GenericForeignKey(ct_field='value_content_type',
                                     fk_field='value_object_id')

    value_ = None  # for None type

    created = models.DateTimeField(_(u"created"), auto_now_add=True)
    modified = models.DateTimeField(_(u"modified"), auto_now=True)

    # ===========================================================

    TYPE_TEXT = 'text'
    TYPE_FLOAT = 'float'
    TYPE_INT = 'int'
    TYPE_DATE = 'date'
    TYPE_BOOLEAN = 'bool'
    TYPE_OBJECT = 'object'
    TYPE_NONE = ''

    DATATYPE_CHOICES = (
        (TYPE_TEXT, _(u"Text")),
        (TYPE_FLOAT, _(u"Float")),
        (TYPE_INT, _(u"Integer")),
        (TYPE_DATE, _(u"Date")),
        (TYPE_BOOLEAN, _(u"True / False")),
        (TYPE_OBJECT, _(u"Django Object")),
        (TYPE_NONE, _(u"None"))
    )

    DATATYPE_VALIDATE = {
        TYPE_TEXT: lambda x: isinstance(x, text_type),
        TYPE_FLOAT: lambda x: isinstance(x, float),
        TYPE_INT: lambda x: isinstance(x, integer_types),
        TYPE_DATE: lambda x: isinstance(x, datetime) or isinstance(x, date),
        TYPE_BOOLEAN: lambda x: isinstance(x, bool),
        TYPE_OBJECT: lambda x: isinstance(x, models.Model),
        TYPE_NONE: lambda x: x is None,
    }

    @classmethod
    def get_type(cls, value):
        for t, f in cls.DATATYPE_VALIDATE.items():
            if f(value):
                return t
        raise TypeError('Unknown value type')

    type = models.CharField(_(u"type"), max_length=10, blank=True,
                            choices=DATATYPE_CHOICES, default=TYPE_NONE)
    name = models.CharField(_(u"name"), max_length=2 ** 8)

    # ===========================================================

    def _get_value(self):
        """
        Return the python object this value is holding
        """
        return getattr(self, 'value_%s' % self.type)

    def _set_value(self, new_value):
        """
        Set the object this value is holding
        """
        # TODO: clean old value type field?
        self.type = self.get_type(new_value)
        setattr(self, 'value_%s' % self.type, new_value)

    value = property(_get_value, _set_value)

    def __unicode__(self):
        return u'%s - %s : %r' % (self.content_object, self.name, self.value)

    class Meta:
        unique_together = (("content_type", "object_id", "name"),)


def set_obj_attr(entity, key, value):
    if not isinstance(entity, models.Model):
        raise TypeError('Django model required')
    if not isinstance(key, text_type):
        raise TypeError('Attr key should be a text type')
    if Attribute.get_type(value) is None:
        raise TypeError('Attr value has an unknown type')

    ct = ContentType.objects.get_for_model(entity)
    pk = entity.pk
    v, created = Attribute.objects.get_or_create(
        object_id=pk, content_type=ct, name=key
    )
    v.value = value
    v.save()
    return created


def get_obj_attr(entity, key):
    if not isinstance(entity, models.Model):
        raise TypeError('Django model required')
    if not isinstance(key, text_type):
        raise TypeError('Attr key should be a text type')

    # TODO: may be get_all_attrs and check key? try think about it
    ct = ContentType.objects.get_for_model(entity)
    pk = entity.pk
    try:
        v = Attribute.objects.get(object_id=pk, content_type=ct, name=key)
    except Attribute.DoesNotExist:
        v = None
    return v


def set_obj_attrs(entity, attrs):
    if not isinstance(entity, models.Model):
        raise TypeError('Django model required')
    for key, value in attrs.items():
        if not isinstance(key, text_type):
            raise TypeError('Entity attr key should be a text type')
        if Attribute.get_type(value) is None:
            raise TypeError('Entity attr value has an unknown type')

    for key, value in attrs.items():
        set_obj_attr(entity, key, value)


def get_obj_attrs(entity):
    if not isinstance(entity, models.Model):
        raise TypeError('Django model required')

    _inject_generic_relation(entity)
    vs = getattr(entity, MODEL_ATTR_FIELD_NAME).all()
    return {v.name: v.value for v in vs}


def filter_by_attrs(qs, **kwargs):
    # TODO: check work with Model objects
    _inject_generic_relation(qs)

    filters = {}
    for attr_name, attr_value in kwargs.items():
        try:
            if isinstance(attr_value, (list, tuple)) and len(attr_value) != 0:
                type = Attribute.get_type(attr_value[0])
                if any(map(lambda x: Attribute.get_type(x) != type,
                           attr_value)):
                    raise TypeError('You can`t use iterable object with '
                                    'different type of items')
            else:
                type = Attribute.get_type(attr_value)
        except TypeError:
            raise TypeError('Unknown type of the "{0}" value'
                            .format(attr_name))

        if USE_FILTER_DATATYPE_DETECT_HEURISTICS:
            # may be wrong detected type for datetime objects
            splitted_attr_name = attr_name.split('__')
            if len(splitted_attr_name) == 2:
                if splitted_attr_name[1] in ['year', 'month', 'day',
                                             'week_day', 'hour', 'minute']:
                    if type != Attribute.TYPE_INT:
                        warn('Strange type detection behavior. Detected {0:!r}'
                             ' but INT expected. DATE type used.'.format(type))

                    type = Attribute.TYPE_DATE

        # TODO: work with Q objects
        field = 'type' if type == Attribute.TYPE_NONE else 'value_' + type
        value = Attribute.TYPE_NONE if type == Attribute.TYPE_NONE \
            else attr_value
        if "__" in attr_name:
            attr_name, attr_filters = attr_name.split('__', 1)
            value_filter = "%s__%s__%s" % (
                MODEL_ATTR_FIELD_NAME, field, attr_filters
            )
        else:
            value_filter = "%s__%s" % (MODEL_ATTR_FIELD_NAME, field)

        filters["%s__name" % MODEL_ATTR_FIELD_NAME] = attr_name
        filters[value_filter] = value

    return qs.filter(**filters)


def prefetch_related_attrs(qs):
    _inject_generic_relation(qs)
    return qs.prefetch_related(MODEL_ATTR_FIELD_NAME)


def _inject_generic_relation(qs_or_model):
    if isinstance(qs_or_model, models.Model):
        model = qs_or_model
    elif isinstance(qs_or_model, models.QuerySet):
        model = qs_or_model.model
    else:
        raise TypeError('Can`t inject generic relation')

    try:
        model._meta.get_field(MODEL_ATTR_FIELD_NAME)
    except FieldDoesNotExist:
        generic_relation = GenericRelation(
            Attribute, related_query_name=MODEL_ATTR_FIELD_NAME)
        generic_relation.contribute_to_class(model, MODEL_ATTR_FIELD_NAME)
