# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_map_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('Objects', models.ManyToManyField(to='maps.MObject')),
            ],
        ),
    ]
