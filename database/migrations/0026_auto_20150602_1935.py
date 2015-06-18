# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0025_auto_20150601_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='receiver_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='sender_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
