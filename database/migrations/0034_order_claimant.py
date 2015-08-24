# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0033_auto_20150801_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='claimant',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
