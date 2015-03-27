# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_auto_20150317_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='lending_product',
            name='returned_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
