# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20150209_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lending_Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('lending_reg', models.ForeignKey(to='database.Lending')),
                ('product', models.ForeignKey(to='database.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Return_Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('product', models.ForeignKey(to='database.Product')),
                ('return_reg', models.ForeignKey(to='database.Return')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='product',
            old_name='amount',
            new_name='in_consignment',
        ),
        migrations.RemoveField(
            model_name='product',
            name='storage',
        ),
        migrations.AddField(
            model_name='input_product',
            name='storage',
            field=models.CharField(default='C', max_length=1, choices=[(b'C', b'Consignacion'), (b'S', b'Stock')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='output_product',
            name='storage',
            field=models.CharField(default='C', max_length=1, choices=[(b'C', b'Consignacion'), (b'S', b'Stock')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='classification',
            field=models.CharField(default='MUELLE', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='in_used',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(default='MAF', max_length=100),
            preserve_default=False,
        ),
    ]
