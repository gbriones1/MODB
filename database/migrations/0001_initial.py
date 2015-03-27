# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appliance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('amount', models.IntegerField()),
                ('storage', models.CharField(max_length=1, choices=[(b'C', b'Consignacion'), (b'S', b'Stock'), (b'U', b'Usadas'), (b'P', b'Prestadas')])),
                ('appliance', models.ManyToManyField(to='database.Appliance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(to='database.Provider'),
            preserve_default=True,
        ),
    ]
