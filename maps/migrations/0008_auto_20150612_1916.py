# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0007_auto_20150612_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobject',
            name='dataset',
            field=models.ForeignKey(related_name='mobjects', to='maps.Dataset'),
        ),
        migrations.AlterField(
            model_name='mobject',
            name='map',
            field=models.ForeignKey(related_name='mobjects', to='maps.Map'),
        ),
    ]
