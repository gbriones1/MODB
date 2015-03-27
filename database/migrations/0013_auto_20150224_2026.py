# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20150224_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input_product',
            name='storage',
        ),
        migrations.RemoveField(
            model_name='output_product',
            name='storage',
        ),
        migrations.AddField(
            model_name='input',
            name='storage',
            field=models.CharField(default='C', max_length=1, choices=[(b'C', b'Consignacion'), (b'S', b'Propias'), (b'U', b'Obsoletas')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='output',
            name='storage',
            field=models.CharField(default='C', max_length=1, choices=[(b'C', b'Consignacion'), (b'S', b'Propias'), (b'U', b'Obsoletas')]),
            preserve_default=False,
        ),
    ]
