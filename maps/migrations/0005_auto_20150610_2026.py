# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_auto_20150609_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='map',
            options={'verbose_name_plural': 'карты', 'verbose_name': 'карта'},
        ),
        migrations.AddField(
            model_name='mobject',
            name='map',
            field=models.ForeignKey(to='maps.Map', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='map',
            name='editors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='editable_maps', blank=True),
        ),
    ]
