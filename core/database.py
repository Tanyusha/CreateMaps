from collections import namedtuple

__author__ = 'Таника'

TableType = namedtuple('TableType', ('TABLE', 'SYSTEM', 'OTHER'))

TableInfo = namedtuple('TableInfo', ('name', 'type', 'columns'))
ColumnInfo = namedtuple('ColumnInfo', ('name', 'table_name', 'type', 'type_size', 'nullable', 'index'))
RelationInfo = namedtuple('RelationInfo', ('table', 'table_fk', 'relation_table', 'relation_table_pk'))
KeyInfo = namedtuple('KeyInfo', ('table_name', 'column_name'))

DatabaseInitInfoType = namedtuple('DatabaseInitInfoType', ('STR', 'INT', 'FLOAT', 'FILEPATH', 'PASSWORD'))


class Database(object):
    @staticmethod
    def required_info_for_init():
        return []

    def relationships(self):
        return NotImplemented

    def tables(self, type=None):
        return NotImplemented

    def execute(self, sql, args=None):
        raise NotImplementedError

    def close(self):
        pass

    # def get_column_type_converter(self, column_type):
    #     pass
    #
    # def get_column_django_model_field(self, column_type):
    #     pass
