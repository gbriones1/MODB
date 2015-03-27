# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20150208_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='product',
        ),
        migrations.RemoveField(
            model_name='input_product',
            name='input_reg',
        ),
        migrations.RemoveField(
            model_name='output',
            name='product',
        ),
        migrations.RemoveField(
            model_name='output_product',
            name='output_reg',
        ),
        migrations.AddField(
            model_name='input',
            name='input_product',
            field=models.ManyToManyField(to='database.Input_Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='output',
            name='output_product',
            field=models.ManyToManyField(to='database.Output_Product'),
            preserve_default=True,
        ),
    ]
