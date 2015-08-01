# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0029_auto_20150722_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='organization',
            field=models.ForeignKey(blank=True, to='database.Organization', null=True),
        ),
    ]
