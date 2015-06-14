from attrs.models import get_obj_attrs, get_obj_attr, set_obj_attr, \
    set_obj_attrs, Attribute, filter_by_attrs, prefetch_related_attrs
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase


class AttrModelTestCase(TestCase):
    def assertValue(self, obj, type, value):
        self.assertEqual(obj.type, type)
        self.assertEqual(obj.value, value)

    def test_get_empty_entity_attrs(self):
        obj = ContentType.objects.get(pk=1)
        res = get_obj_attrs(obj)
        self.assertEqual(res, {})

    def test_set_and_get_attr(self):
        obj = ContentType.objects.get(pk=1)
        value = get_obj_attr(obj, 'test')
        self.assertEqual(value, None)
        is_set = set_obj_attr(obj, 'test', 1)
        self.assertTrue(is_set)
        value = get_obj_attr(obj, 'test')
        self.assertValue(value, Attribute.TYPE_INT, 1)

    def test_set_and_get_attrs(self):
        obj = ContentType.objects.get(pk=1)
        set_obj_attrs(obj, {'Color': 'Black', 'Width': 200})
        res = get_obj_attrs(obj)
        self.assertEqual(res, {'Color': 'Black', 'Width': 200})

    def test_del_field(self):
        pass

    def test_simple_filter(self):
        obj = ContentType.objects.get(pk=1)
        obj2 = ContentType.objects.get(pk=2)

        set_obj_attrs(obj, {'width': 200})
        set_obj_attrs(obj2, {'width': 400})

        r = filter_by_attrs(ContentType.objects.all(), width=200)[0]
        self.assertEqual(r.pk, obj.pk)

    def test_filter__gt__lt(self):
        obj = ContentType.objects.get(pk=1)
        obj2 = ContentType.objects.get(pk=2)

        set_obj_attrs(obj, {'width': 200})
        set_obj_attrs(obj2, {'width': 400})

        r = filter_by_attrs(ContentType.objects.all(), width__gt=100).count()
        self.assertEqual(r, 2)

        r = filter_by_attrs(ContentType.objects.all(), width__lt=1000).count()
        self.assertEqual(r, 2)

        r = filter_by_attrs(ContentType.objects.all(), width__gt=300).count()
        self.assertEqual(r, 1)

        r = filter_by_attrs(ContentType.objects.all(), width__lt=300).count()
        self.assertEqual(r, 1)

    def test_unicode_name_filter(self):
        obj = ContentType.objects.get(pk=1)

        set_obj_attrs(obj, {u'тест': 200})
        r = filter_by_attrs(ContentType.objects.all(), **{u'тест': 200})[0]
        self.assertEqual(r.id, 1)

    def test_filter__in(self):
        obj = ContentType.objects.get(pk=1)
        obj2 = ContentType.objects.get(pk=2)

        set_obj_attrs(obj, {'width': 200})
        set_obj_attrs(obj2, {'width': 400})

        r = filter_by_attrs(ContentType.objects.all(), width__in=[200, 400])
        self.assertEqual(r.count(), 2)

    def test_filter__contains(self):
        obj = ContentType.objects.get(pk=1)
        obj2 = ContentType.objects.get(pk=2)

        set_obj_attrs(obj, {'tags': 'milk, tee'})
        set_obj_attrs(obj2, {'tags': 'milk'})

        r = filter_by_attrs(ContentType.objects.all(), tags__contains='milk')
        self.assertEqual(r.count(), 2)
        r = filter_by_attrs(ContentType.objects.all(), tags__contains='tee')
        self.assertEqual(r.count(), 1)

    def test_prefetch_related(self):
        obj = ContentType.objects.get(pk=1)
        obj2 = ContentType.objects.get(pk=2)

        set_obj_attrs(obj, {'tags': 'milk, tee', 'width': 1, 'is_ok': True})
        set_obj_attrs(obj2, {'tags': 'milk', 'is_ok': False})

        with self.assertNumQueries(2):
            qs = []
            for x in prefetch_related_attrs(ContentType.objects.filter(id__in=[1, 2])):
                qs.append(get_obj_attrs(x))

        # self.assertEqual(len(qs), 2)
        self.assertEqual(qs, [{'tags': 'milk, tee', 'width': 1, 'is_ok': True},
                              {'tags': 'milk', 'is_ok': False}])

        # TODO: write test with models

"""
exact
iexact
contains
icontains
in
gt
gte
lt
lte
startswith
istartswith
endswith
iendswith
range
year
month
day
week_day
hour
minute
second
isnull
search
regex
iregex
"""
