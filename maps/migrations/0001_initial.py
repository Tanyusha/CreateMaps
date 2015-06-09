# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=512)),
                ('datasets', models.ManyToManyField(to='maps.Dataset')),
                ('filters', models.ManyToManyField(to='maps.Filter')),
            ],
        ),
        migrations.CreateModel(
            name='MObject',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('type', models.IntegerField(default=1, choices=[(1, 'point'), (2, 'polygon')])),
                ('data', django.contrib.postgres.fields.hstore.HStoreField()),
                ('dataset', models.ForeignKey(to='maps.Dataset')),
            ],
        ),
    ]
