from django.template.loader import get_template
import os
import pypyodbc

from django.template import Context, Template


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_project_.settings")
from django.conf import settings




db_file = r'C:\Users\Tanika\PycharmProjects\CreateMaps\base.mdb'
user = 'admin'
password = 'Masterkey1'
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s;unicode_results=True' % \
                (db_file, user, password)

# pypyodbc.win_create_mdb('D:\\database.mdb')

# connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\database.mdb'

conn = pypyodbc.connect(odbc_conn_str)
c = conn.cursor()
c2 = conn.cursor()

# c.execute("select * from MSysRelationships;")
# rows = c.fetchall()
# for row in rows:
#     print(row)

lots = []
c.execute("select ОПИ_Участки.Наименование, ОПИ_Участки.[Координата-широта], ОПИ_Участки.[Координата-долгота] from ОПИ_Участки;")
rows = c.fetchall()
for row in rows:
    if not row[1] or not row[2]:
        continue
    # coords = [row[1], row[2]]
    if not row[0]:
        lot = {'name':'', 'coords':[row[1], row[2]]}
    else:
        lot = {'name':row[0], 'coords':[row[1], row[2]]}
    lots.append(lot)
# print(lots)
#
# print(len(lots))


t = get_template('index.html')

c = Context({"lots": lots})
f = open('gg.html', 'w', encoding='utf-8')
f.write(t.render(c))
f.close()

def work_with_database(c, c2):
    for x in c.tables():
        print('-' * 20)
        # print(type(x))
        table_cat = x.get('table_cat')
        table_schema = x.get('table_schema')
        table_name = x.get('table_name')
        table_type = x.get('table_type')
        remarks = x.get('remarks')
        print(x[1:])
        print(table_cat, table_schema, table_name, table_type, remarks)
        for y in c2.columns(table_name):
            table_cat = y.get('table_cat')
            table_schem = y.get('table_schem')
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
            # print(table_qualifier, table_schem, table_name, column_name, data_type, type_name, precision, length, scale,
            # radix, nullable, remarks)
            print(table_schem, table_name, column_name, data_type, type_name, column_size, buffer_length,
                  decimal_digits, num_prec_radix, nullable, remarks, column_def, sql_data_type, sql_datetime_sub,
                  char_octet_length, ordinal_position, is_nullable)
            print(c2.getTypeInfo(data_type))


# work_with_database(c, c2)