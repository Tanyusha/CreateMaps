# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_auto_20150614_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='type',
            field=models.CharField(default='', choices=[('text', 'Text'), ('float', 'Float'), ('int', 'Integer'), ('date', 'Date'), ('bool', 'True / False'), ('object', 'Django Object'), ('', 'None')], max_length=10),
            preserve_default=False,
        ),
    ]
