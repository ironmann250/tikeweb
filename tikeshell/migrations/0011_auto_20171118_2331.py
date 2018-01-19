# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 15:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikeshell', '0010_auto_20171118_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickettype',
            name='event',
        ),
        migrations.AddField(
            model_name='show',
            name='tickettypes',
            field=models.ManyToManyField(to='tikeshell.tickettype'),
        ),
        migrations.AlterField(
            model_name='show',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 18, 23, 31, 4, 392000)),
        ),
        migrations.AlterField(
            model_name='show',
            name='likes',
            field=models.BigIntegerField(default=1292),
        ),
        migrations.AlterField(
            model_name='show',
            name='stars',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='show',
            name='views',
            field=models.BigIntegerField(default=2414),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 18, 23, 31, 4, 400000)),
        ),
    ]
