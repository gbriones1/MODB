# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20150223_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='return_product',
            name='product',
        ),
        migrations.RemoveField(
            model_name='return_product',
            name='return_reg',
        ),
        migrations.DeleteModel(
            name='Return',
        ),
        migrations.DeleteModel(
            name='Return_Product',
        ),
        migrations.AddField(
            model_name='lending',
            name='destination',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lending',
            name='employee',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lending',
            name='returned',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='is_used',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='classification',
            field=models.ForeignKey(blank=True, to='database.Classification', null=True),
            preserve_default=True,
        ),
    ]
