import string
from _project_.consts import STEP_1_FILEPATH, STEP_2_DATABASE_INIT_DATA
from core import DATABESE_TYPES
from django.shortcuts import render, redirect
from maps.models import Map
import os
import functools
import random


def add_db_to_request(fn):
    @functools.wraps(fn)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'error-user-is-not-authenticated.html')

        path = request.session.get(STEP_1_FILEPATH)
        filename = os.path.basename(path)

        name, ext = os.path.splitext(filename)
        DBase = DATABESE_TYPES.get(ext)
        if not DBase:
            return render(request, 'error-db-not-supported.html')

        request.DBase = DBase

        init_data = request.session.get(STEP_2_DATABASE_INIT_DATA)
        if not init_data:
            return redirect('step2')

        request.db = db = DBase(**init_data)
        request.db_filename = filename
        map_id = request.session.get('step-3-map-id')
        request.map = Map.objects.filter(id=map_id) if map_id else None
        response = fn(request, *args, **kwargs)
        db.close()
        return response

    return _wrapper


def generate_random_string(length=8):
    return ''.join([random.choice(string.hexdigits)
                    for _ in range(10)])
