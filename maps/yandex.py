from __future__ import unicode_literals, print_function, generators, division
import functools
from django.template.defaultfilters import pprint
import operator


def create_yandex_point_object(point_id, coords, **kwargs):
    name = "Объект: {0}".format(point_id)
    body = pprint(kwargs)
    proper = {
        "balloonContent": '<pre>{1}</pre>'.format(name, body),
        "clusterCaption": name,
        "hintContent": "Текст подсказки",
    }
    proper.update(kwargs)
    point_json = {
        "type": "Feature",
        "id": point_id,
        "geometry": {
            "type": "Point",
            "coordinates": coords
        },
        "properties": proper
    }
    return point_json


def create_yandex_poinrs_objects(objs, lat_getter=operator.itemgetter('lat'),
                                 lon_getter=operator.itemgetter('lon'),
                                 data_getter=operator.itemgetter('data')):
    points = []
    for i, obj in enumerate(objs):
        # d = {'lat': latitude, 'lon': longitude, 'data': data}
        lat = lat_getter(obj)
        lon = lon_getter(obj)
        data = data_getter(obj)
        p = create_yandex_point_object(i, [lat, lon], **data)
        points.append(p)

    json_points = {
        "type": "FeatureCollection",
        "features": points
    }

    return json_points
