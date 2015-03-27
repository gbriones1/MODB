# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20150223_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lending_product',
            old_name='lending_reg',
            new_name='lending',
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='is_used',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
