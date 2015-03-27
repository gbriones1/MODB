# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_auto_20150224_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('provider', models.ForeignKey(to='database.Provider')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('order', models.ForeignKey(to='database.Order')),
                ('product', models.ForeignKey(to='database.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lending',
            name='returned_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lending',
            name='storage',
            field=models.CharField(default='S', max_length=1, choices=[(b'C', b'Consignacion'), (b'S', b'Propias'), (b'U', b'Obsoletas')]),
            preserve_default=False,
        ),
    ]
