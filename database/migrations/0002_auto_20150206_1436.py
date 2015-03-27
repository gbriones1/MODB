# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='appliance',
            field=models.ManyToManyField(to='database.Appliance', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(blank=True, to='database.Provider', null=True),
            preserve_default=True,
        ),
    ]
