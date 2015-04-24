# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='used_tobe',
        ),
        migrations.AddField(
            model_name='output',
            name='destination',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='output',
            name='employee',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=1, choices=[(b'P', b'Por pedir'), (b'A', b'Pedido'), (b'C', b'Cancelado'), (b'R', b'Recibido')]),
            preserve_default=True,
        ),
    ]
