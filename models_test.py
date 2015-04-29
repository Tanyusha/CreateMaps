import os
import django
from django.conf import settings
from django import db
from django.db import models
from django.db.backends.sqlite3.base import DatabaseSchemaEditor, DatabaseIntrospection
from django.db import migrations

__author__ = 'Таника'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_project_.settings")
django.setup()


print(db.connection)
print(db.connections.all())


def do(editor):
    """
    :type editor: DatabaseSchemaEditor
    :return:
    """


class Some(models.Model):
    class Meta:
        app_label = 'qw'

# db.connection.introspection
editor = db.connection.schema_editor()
""":type editor: DatabaseSchemaEditor"""
# with editor:
#     editor.create_model(Some)


# editor.close()
