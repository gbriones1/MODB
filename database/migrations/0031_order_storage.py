# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0030_order_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='storage',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'C', b'Consignacion'), (b'S', b'Propias'), (b'U', b'Obsoletas')]),
        ),
    ]
