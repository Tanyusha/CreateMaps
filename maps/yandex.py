from __future__ import unicode_literals, print_function, generators, division


def create_yandex_point_object(point_id, coords, name, **kwargs):
    proper = {
        "balloonContent": '<h3>' + name + "</h3>",
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
        p = create_yandex_point_object(i, [lat, lon], '', **data)
        points.append(p)

    json_points = {
        "type": "FeatureCollection",
        "features": points
    }

    return json_points
