# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0032_auto_20150731_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='received_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order_product',
            name='received_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order_product',
            name='status',
            field=models.CharField(max_length=1, null=True, choices=[(b'P', b'Por pedir'), (b'A', b'Pedido'), (b'C', b'Cancelado'), (b'R', b'Recibido')]),
        ),
    ]
