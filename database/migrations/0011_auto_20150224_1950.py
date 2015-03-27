# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20150224_1931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock',
            new_name='consingment_tobe',
        ),
        migrations.AddField(
            model_name='product',
            name='stock_tobe',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='used_tobe',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
