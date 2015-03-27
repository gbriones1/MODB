# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20150224_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_used',
        ),
        migrations.AlterField(
            model_name='lending',
            name='returned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
