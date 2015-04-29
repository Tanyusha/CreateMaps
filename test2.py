from core.mdb import MDBDatabase
import os
import utils


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_project_.settings")

# ---------------------Подключение к базе данных------------------------
db_file = r'C:\Users\Tanika\PycharmProjects\CreateMaps\base.mdb'
user = 'admin'
password = 'Masterkey1'

conn = utils.make_mdb_odbc_connection(db_file, user, password)
c = utils.make_cursor(conn)

# ---------------------Функция преобразования данных в формат, пригодный для наложения на Яндекс.Карту------------------------
def create_yandex_point_object(point_id, coords, name, lala):
    point_json = {
        "type": "Feature",
        "id": point_id,
        "geometry": {
            "type": "Point",
            "coordinates": coords
        },
        "properties": {
            "balloonContent": '<h3>'+name+"</h3>",
            "clusterCaption": name,
            "hintContent": "Текст подсказки",
            "name": lala
        }
    }
    return point_json

# ---------------------Считывание данных из базы и формирование объектов для наложения на карту------------------------
points = []
# c.execute(
#     "select ОПИ_Участки.ИДУчастка, ОПИ_Участки.Наименование, ОПИ_Участки.[Координата-широта], ОПИ_Участки.[Координата-долгота] from ОПИ_Участки;")


# for row in rows:
#     if not row[2] or not row[3]:
#         continue
#     name = row[1] if row[1] else ''
#     coords = [float(row[2].replace(',', '.')), float(row[3].replace(',', '.'))]
#     id_ = row[0]
#     if count %2 == 0:
#         lala = "Tanya"
#     else:
#         lala = 'Pasha'
#     count += 1
#
#     point = create_yandex_point_object(id_, coords, name, lala)
#     points.append(point)
# # print(points)
# json_points = {
#   "type": "FeatureCollection",
#   "features": points
# }
#
# print(json_points)
#
# # ---------------------Создание файла data.json для наложения объектов на карту------------------------
# json_points = json.dumps(json_points, separators=(',', ':'))
# f = open('_project_/static/data.json', 'w')
# f.write(json_points)
# f.close()

types = set()

# ---------------------Тестирование работы с бд------------------------
def work_with_database(c, c2):
    for x in c.tables():

        # print(type(x))
        table_cat = x.get('table_cat')
        table_schema = x.get('table_schema')
        table_name = x.get('table_name')
        table_type = x.get('table_type')
        remarks = x.get('remarks')
        # if not table_name.startswith('M'):
        #     continue
        print('-' * 20)
        print(x[1:])
        # print(table_cat, table_schema, table_name, table_type, remarks)
        for y in c2.columns(table_name):
            table_cat = y.get('table_cat')
            table_schem = y.get('table_schema')
            table_name = y.get('table_name')
            column_name = y.get('column_name')
            data_type = y.get('data_type')
            type_name = y.get('type_name')
            column_size = y.get('column_size')
            buffer_length = y.get('buffer_length')
            decimal_digits = y.get('decimal_digits')
            num_prec_radix = y.get('num_prec_radix')
            nullable = y.get('nullable')
            remarks = y.get('remarks')
            column_def = y.get('column_def')
            sql_data_type = y.get('sql_data_type')
            sql_datetime_sub = y.get('sql_datetime_sub')
            char_octet_length = y.get('char_octet_length')
            ordinal_position = y.get('ordinal_position')
            is_nullable = y.get('is_nullable')
            # print(y[1:])
            # types.add(type_name)
            # print(table_qualifier, table_schem, table_name, column_name, data_type, type_name, precision, length, scale,
            # radix, nullable, remarks)
            # print(table_schem, table_name, column_name, data_type, type_name, column_size, buffer_length,
            #       decimal_digits, num_prec_radix, nullable, remarks, column_def, sql_data_type, sql_datetime_sub,
            #       char_octet_length, ordinal_position, is_nullable)
            # print(c2.getTypeInfo(data_type))


# c2 = utils.make_cursor(conn)
# work_with_database(c, c2)
# print(types)

# первое слово - поле - внешний ключ, ссылающийся на 2-ю таблицу. второе слово - название таблицы с внешним ключом
# третье слово - поле - идентификатор 2-ой таблицы, на который ссылается внешний ключ. Четвертое слово - название таблицы, на которую ссылается первая таблица.
mdb = MDBDatabase(db_file, user, password)
cols = mdb.tables()['MSysRelationships'].columns
# print(list(x.name for x in cols))
print(mdb.relationships())
