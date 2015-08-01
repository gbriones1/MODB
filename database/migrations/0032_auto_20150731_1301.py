# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0031_order_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='order',
            name='storage',
        ),
        migrations.AddField(
            model_name='order_product',
            name='organization',
            field=models.ForeignKey(blank=True, to='database.Organization', null=True),
        ),
        migrations.AddField(
            model_name='order_product',
            name='storage',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'C', b'Consignacion'), (b'S', b'Propias'), (b'U', b'Obsoletas')]),
        ),
    ]
