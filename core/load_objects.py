from __future__ import unicode_literals, print_function, generators, division
import json
import os

__author__ = 'pahaz'


def load_objects(path):
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            j = json.loads(f.read())
            return j
    else:
        return []


def bump_objects(path, objects):
    if not isinstance(objects, list):
        raise RuntimeError('list required')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(objects))
