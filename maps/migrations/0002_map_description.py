# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='description',
            field=models.TextField(default='no'),
            preserve_default=False,
        ),
    ]
