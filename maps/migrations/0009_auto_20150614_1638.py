# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0008_auto_20150612_1916'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attr',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='attr',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='attr',
            name='entity_type',
        ),
        migrations.RemoveField(
            model_name='attr',
            name='schema',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='schema',
        ),
        migrations.AlterField(
            model_name='field',
            name='map',
            field=models.ForeignKey(to='maps.Map', related_name='fields'),
        ),
        migrations.AlterField(
            model_name='point',
            name='object',
            field=models.ForeignKey(to='maps.MObject', related_name='points'),
        ),
        migrations.DeleteModel(
            name='Attr',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Schema',
        ),
    ]
