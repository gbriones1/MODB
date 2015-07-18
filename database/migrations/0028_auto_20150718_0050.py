# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0027_auto_20150717_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='input',
            name='invoice_number',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='appliance',
            field=models.ManyToManyField(to='database.Appliance', blank=True),
        ),
    ]
