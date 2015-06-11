from __future__ import unicode_literals, print_function, generators, division
from django.template.defaultfilters import pprint


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


def create_yandex_poinrs_objects(objs):
    points = []
    for i, obj in enumerate(objs):
        # d = {'lat': latitude, 'lon': longitude, 'data': data}
        lat = obj['lat']
        lon = obj['lon']
        data = obj['data']
        p = create_yandex_point_object(i, [lat, lon], **data)
        points.append(p)

    json_points = {
        "type": "FeatureCollection",
        "features": points
    }

    return json_points
