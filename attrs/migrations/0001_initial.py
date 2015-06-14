# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('entity_id', models.IntegerField()),
                ('value_text', models.TextField(null=True, blank=True)),
                ('value_float', models.FloatField(null=True, blank=True)),
                ('value_int', models.IntegerField(null=True, blank=True)),
                ('value_date', models.DateTimeField(null=True, blank=True)),
                ('value_bool', models.NullBooleanField()),
                ('value_object_id', models.IntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(blank=True, verbose_name='type', null=True, choices=[('text', 'Text'), ('float', 'Float'), ('int', 'Integer'), ('date', 'Date'), ('bool', 'True / False'), ('object', 'Django Object')], max_length=10)),
                ('name', models.CharField(blank=True, verbose_name='name', null=True, max_length=256)),
                ('entity_ct', models.ForeignKey(related_name='value_entities', to='contenttypes.ContentType')),
                ('value_object_ct', models.ForeignKey(related_name='value_objects', blank=True, to='contenttypes.ContentType', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='value',
            unique_together=set([('entity_ct', 'entity_id', 'name')]),
        ),
    ]
