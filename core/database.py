from collections import namedtuple

__author__ = 'Таника'

TableType = namedtuple('TableType', ('TABLE', 'SYSTEM', 'OTHER'))
ColumnInfo = namedtuple('ColumnInfo', ('name', 'type', 'index', 'size', 'django_field_type', 'nullable', 'converter'))
TableInfo = namedtuple('TableInfo', ('name', 'type', 'columns'))
RelationInfo = namedtuple('RelationInfo', ('table', 'table_fk', 'relation_table', 'relation_table_pk'))
DatabaseInitInfoType = namedtuple('DatabaseInitInfoType', ('STR', 'INT', 'FLOAT', 'FILEPATH', 'PASSWORD'))


class Database(object):
    @staticmethod
    def required_info_for_init():
        return {}

    def relationships(self):
        return NotImplemented

    def tables(self):
        return NotImplemented

    def execute(self, sql, args):
        raise NotImplementedError

    def close(self):
        pass
