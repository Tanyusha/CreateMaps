# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0003_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('is_required', models.BooleanField(default=False)),
                ('is_filter', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('object', models.ForeignKey(to='maps.MObject')),
            ],
        ),
        migrations.RemoveField(
            model_name='points',
            name='Objects',
        ),
        migrations.RemoveField(
            model_name='map',
            name='datasets',
        ),
        migrations.RemoveField(
            model_name='map',
            name='filters',
        ),
        migrations.AddField(
            model_name='dataset',
            name='map',
            field=models.ForeignKey(to='maps.Map', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='map',
            name='editors',
            field=models.ManyToManyField(related_name='editable_maps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='map',
            name='user',
            field=models.ForeignKey(default=1, related_name='ownable_maps', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Filter',
        ),
        migrations.DeleteModel(
            name='Points',
        ),
        migrations.AddField(
            model_name='field',
            name='map',
            field=models.ForeignKey(to='maps.Map'),
        ),
    ]
