from __future__ import unicode_literals, print_function, generators, division
from core.load_objects import load_objects, dump_objects
import os
from django.conf import settings
from maps.models import Map


def load_map_objs(map):
    if not isinstance(map, Map):
        raise TypeError('Map object required')
    DATA_FILE = os.path.join(settings.MEDIA_ROOT,
                             'data{0}.json'.format(map.id))
    objs = load_objects(DATA_FILE)
    return objs


def dump_map_objs(map, objs):
    if not isinstance(map, Map):
        raise TypeError('Map object required')
    DATA_FILE = os.path.join(settings.MEDIA_ROOT,
                             'data{0}.json'.format(map.id))
    dump_objects(DATA_FILE, objs)
