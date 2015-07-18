# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0026_auto_20150602_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Percentage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_price_limit', models.DecimalField(max_digits=9, decimal_places=2)),
                ('percentage_1', models.DecimalField(max_digits=9, decimal_places=2)),
                ('percentage_2', models.DecimalField(max_digits=9, decimal_places=2)),
                ('percentage_3', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='classification',
        ),
    ]
