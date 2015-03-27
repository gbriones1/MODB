# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20150224_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='consingment_tobe',
            new_name='consignment_tobe',
        ),
    ]
