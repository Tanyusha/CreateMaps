# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import eav.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('maps', '0006_auto_20150610_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('entity_id', models.IntegerField()),
                ('value_text', models.TextField(null=True, blank=True)),
                ('value_float', models.FloatField(null=True, blank=True)),
                ('value_date', models.DateField(null=True, blank=True)),
                ('value_bool', models.NullBooleanField()),
                ('value_range_min', models.FloatField(null=True, blank=True)),
                ('value_range_max', models.FloatField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'attributes',
                'verbose_name': 'attribute',
                'ordering': ['entity_type', 'entity_id', 'schema'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(help_text='user-friendly attribute name', max_length=250, verbose_name='title')),
                ('name', autoslug.fields.AutoSlugField(populate_from='title', blank=True, editable=True, slugify=eav.models.slugify_attr_name, verbose_name='name')),
                ('help_text', models.CharField(help_text='short description for administrator', max_length=250, verbose_name='help text', blank=True)),
                ('datatype', models.CharField(max_length=5, choices=[('text', 'text'), ('float', 'number'), ('date', 'date'), ('bool', 'boolean'), ('one', 'choice'), ('many', 'multiple choices'), ('range', 'numeric range')], verbose_name='data type')),
                ('required', models.BooleanField(default=False, verbose_name='required')),
                ('searched', models.BooleanField(default=False, verbose_name='include in search')),
                ('filtered', models.BooleanField(default=False, verbose_name='include in filters')),
                ('sortable', models.BooleanField(default=False, verbose_name='allow sorting')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'schemata',
                'verbose_name': 'schema',
                'ordering': ['title'],
            },
        ),
        migrations.RemoveField(
            model_name='mobject',
            name='data',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='map',
            field=models.ForeignKey(related_name='datasets', to='maps.Map'),
        ),
        migrations.AddField(
            model_name='choice',
            name='schema',
            field=models.ForeignKey(related_name='choices', to='maps.Schema'),
        ),
        migrations.AddField(
            model_name='attr',
            name='choice',
            field=models.ForeignKey(null=True, related_name='attrs', to='maps.Choice'),
        ),
        migrations.AddField(
            model_name='attr',
            name='entity_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='attr',
            name='schema',
            field=models.ForeignKey(related_name='attrs', to='maps.Schema'),
        ),
        migrations.AlterUniqueTogether(
            name='attr',
            unique_together=set([('entity_type', 'entity_id', 'schema', 'choice')]),
        ),
    ]
