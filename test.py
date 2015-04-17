# encoding=cp1251

import pyodbc

db_file = r'C:\Users\Tanika\PycharmProjects\CreateMaps\base.mdb'

user = 'admin'

password = 'Masterkey1'

odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s;unicode_results=True' % \
                (db_file, user, password)

conn = pyodbc.connect(odbc_conn_str)

# conn.execute("SET NAMES='UTF8'")
# conn.execute("SET client_encoding='UTF-8'")

c = conn.cursor()
c2 = conn.cursor()

for x in c.tables():
    print('-'*20)
    print(x.table_name)
    # # print(x.table_schem)
    print(type(x.table_name))
    for row in c2.columns(table=x.table_name.encode('cp1251')):
        print(row.column_name)



print("gfhf")
c.execute("select * from base.ОКАТО")
