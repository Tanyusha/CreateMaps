# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
