# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20150610_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobject',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mobject',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
