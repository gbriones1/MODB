# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_auto_20150320_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='P', max_length=1, choices=[(b'P', b'Pedido'), (b'C', b'Cancelado'), (b'R', b'Recibido')]),
            preserve_default=False,
        ),
    ]
