# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0010_field_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='type',
        ),
    ]
