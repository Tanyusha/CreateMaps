# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attrs', '0002_auto_20150613_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(verbose_name='name', max_length=256),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='type',
            field=models.CharField(verbose_name='type', default='', max_length=10, blank=True, choices=[('text', 'Text'), ('float', 'Float'), ('int', 'Integer'), ('date', 'Date'), ('bool', 'True / False'), ('object', 'Django Object'), ('', 'None')]),
        ),
    ]
