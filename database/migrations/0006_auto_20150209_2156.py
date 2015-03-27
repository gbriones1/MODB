# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20150209_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='input_product',
        ),
        migrations.RemoveField(
            model_name='output',
            name='output_product',
        ),
        migrations.AddField(
            model_name='input_product',
            name='input_reg',
            field=models.ForeignKey(default=1, to='database.Input'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='output_product',
            name='output_reg',
            field=models.ForeignKey(default=1, to='database.Output'),
            preserve_default=False,
        ),
    ]
