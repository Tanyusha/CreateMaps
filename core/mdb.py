from core.database import Database, TableType, ColumnInfo, TableInfo, RelationInfo, DatabaseInitInfoType
import pypyodbc

ODBC_TO_DJANGO = {
    pypyodbc.SQL_TYPE_NULL: 'NullBooleanField',
    pypyodbc.SQL_BIGINT: 'BigIntegerField',
    pypyodbc.SQL_BINARY: 'BinaryField',
    pypyodbc.SQL_BIT: 'NullBooleanField',
    pypyodbc.SQL_CHAR: 'CharField',
    pypyodbc.SQL_DECIMAL: 'DecimalField',
    pypyodbc.SQL_DOUBLE: 'FloatField',
    pypyodbc.SQL_FLOAT: 'FloatField',
    pypyodbc.SQL_GUID: 'CharField',  # !
    pypyodbc.SQL_INTEGER: 'IntegerField',
    pypyodbc.SQL_LONGVARBINARY: 'BinaryField',
    pypyodbc.SQL_NUMERIC: 'DecimalField',
    pypyodbc.SQL_REAL: 'FloatField',
    pypyodbc.SQL_SMALLINT: 'SmallIntegerField',
    pypyodbc.SQL_TINYINT: 'SmallIntegerField',
    pypyodbc.SQL_TYPE_DATE: 'DateField',
    pypyodbc.SQL_DATE: 'DateField',
    pypyodbc.SQL_TYPE_TIME: 'TimeField',
    pypyodbc.SQL_TIME: 'TimeField',
    pypyodbc.SQL_SS_TIME2: 'TimeField',
    pypyodbc.SQL_TYPE_TIMESTAMP: 'DateTimeField',
    pypyodbc.SQL_TIMESTAMP: 'DateTimeField',
    pypyodbc.SQL_VARBINARY: 'BinaryField',
    pypyodbc.SQL_VARCHAR: 'TextField',
    pypyodbc.SQL_LONGVARCHAR: 'TextField',
    pypyodbc.SQL_SS_VARIANT: 'TextField',
    pypyodbc.SQL_SS_UDT: 'TextField',
    pypyodbc.SQL_SS_XML: 'TextField',
    pypyodbc.SQL_WCHAR: 'CharField',
    pypyodbc.SQL_WLONGVARCHAR: 'TextField',
    pypyodbc.SQL_WVARCHAR: 'TextField',
}

ODBC_TO_DATABASE_TABLE_TYPE = {
    'SYSTEM TABLE': TableType.SYSTEM,
    'TABLE': TableType.TABLE,
}


def make_mdb_odbc_connection(db_file, user, password):
    odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s;unicode_results=True' % \
                    (db_file, user, password)
    return pypyodbc.connect(odbc_conn_str)


def make_cursor(conn):
    return conn.cursor()


class MDBDatabase(Database):
    @staticmethod
    def required_info_for_init():
        return [
            ('file', DatabaseInitInfoType.FILEPATH),
            ('username', DatabaseInitInfoType.STR),
            ('password', DatabaseInitInfoType.PASSWORD),
        ]

    def __init__(self, file, username, password):
        self._conn = make_mdb_odbc_connection(file, username, password)

    def tables(self, type=None):
        c = make_cursor(self._conn)
        c2 = make_cursor(self._conn)
        tables = {}
        for x in c.tables():
            table_name = x.get('table_name')
            table_type = x.get('table_type')
            table_type = ODBC_TO_DATABASE_TABLE_TYPE.get(table_type, TableType.OTHER)
            if type and type != table_type:
                continue

            table_cols = []
            for i, y in enumerate(c2.columns(table_name)):
                column_name = y.get('column_name')
                column_size = y.get('column_size')
                # buffer_length = y.get('buffer_length')
                sql_data_type = y.get('sql_data_type')
                nullable = bool(y.get('nullable'))
                data_type, converter, buffer_type, buffer_allocator, default_size, variable_length = \
                    pypyodbc.SQL_data_type_dict.get(sql_data_type)
                django_field_type = ODBC_TO_DJANGO.get(sql_data_type)
                table_cols.append(ColumnInfo(
                    name=column_name,
                    type=data_type,
                    index=i,
                    size=max(column_size, default_size) if variable_length else None,
                    django_field_type=django_field_type,
                    nullable=nullable,
                    converter=converter,
                ))
            tables[table_name] = TableInfo(
                name=table_name,
                type=table_type,
                columns=table_cols,
            )
        c2.close()
        c.close()
        return tables

    def relationships(self):
        c = make_cursor(self._conn)
        c.execute("SELECT * FROM MSysRelationships")
        rows = c.fetchall()
        relations = {}
        for x in rows:
            szColumn, szObject, szReferencedColumn, szReferencedObject = 3, 4, 5, 6
            table = x[szObject]
            table_column_fk = x[szColumn]
            relation_table = x[szReferencedObject]
            relation_table_pk = x[szReferencedObject]

            relations.setdefault(table, [])
            relations[table].append(RelationInfo(table, table_column_fk, relation_table, relation_table_pk))
        c.close()
        return relations

    def close(self):
        self._conn.close()
