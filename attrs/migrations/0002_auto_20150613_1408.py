# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('attrs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('value_text', models.TextField(blank=True, null=True)),
                ('value_float', models.FloatField(blank=True, null=True)),
                ('value_int', models.IntegerField(blank=True, null=True)),
                ('value_date', models.DateTimeField(blank=True, null=True)),
                ('value_bool', models.NullBooleanField()),
                ('value_object_id', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(verbose_name='created', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(choices=[('text', 'Text'), ('float', 'Float'), ('int', 'Integer'), ('date', 'Date'), ('bool', 'True / False'), ('object', 'Django Object')], blank=True, verbose_name='type', max_length=10, null=True)),
                ('name', models.CharField(blank=True, verbose_name='name', max_length=256, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('value_content_type', models.ForeignKey(blank=True, related_name='attribute_value_set', null=True, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='value',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='value',
            name='entity_ct',
        ),
        migrations.RemoveField(
            model_name='value',
            name='value_object_ct',
        ),
        migrations.DeleteModel(
            name='Value',
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set([('content_type', 'object_id', 'name')]),
        ),
    ]
