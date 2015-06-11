from __future__ import unicode_literals, print_function, generators, division
from datetime import datetime
import json
from json import JSONDecoder, JSONEncoder
import os


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = type
            return d


class DateTimeEncoder(JSONEncoder):
    """ Instead of letting the default encoder convert datetime to string,
        convert datetime objects into a dict, which can be decoded by the
        DateTimeDecoder
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            return JSONEncoder.default(self, obj)


def load_objects(path):
    if os.path.exists(path):
        try:
            with open(path, encoding='utf-8') as f:
                j = loads(f.read())
                return j
        except:
            dump_objects(path, [])
            return []
    else:
        return []


def dump_objects(path, objects):
    if not isinstance(objects, list):
        raise RuntimeError('list required')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dumps(objects))


def loads(s):
    return json.loads(s, cls=DateTimeDecoder)


def dumps(o):
    return json.dumps(o, cls=DateTimeEncoder)
