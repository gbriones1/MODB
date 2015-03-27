# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_lending_product_returned_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='email',
            new_name='receiver_email',
        ),
        migrations.AddField(
            model_name='configuration',
            name='sender_email',
            field=models.EmailField(max_length=75, null=True),
            preserve_default=True,
        ),
    ]
