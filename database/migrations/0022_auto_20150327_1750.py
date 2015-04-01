# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_auto_20150327_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lending_Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('returned_amount', models.IntegerField()),
                ('lending', models.ForeignKey(to='database.Lending')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('code', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('condition', models.CharField(max_length=255, null=True, blank=True)),
                ('amount', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lending_tool',
            name='tool',
            field=models.ForeignKey(to='database.Tool'),
            preserve_default=True,
        ),
    ]
