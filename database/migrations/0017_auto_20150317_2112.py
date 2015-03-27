# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_auto_20150317_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='input_product',
            name='price',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='output_product',
            name='price',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2),
            preserve_default=False,
        ),
    ]
