# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 15:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikeshell', '0011_auto_20171118_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_type',
        ),
        migrations.AlterField(
            model_name='show',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 18, 23, 33, 12, 62000)),
        ),
        migrations.AlterField(
            model_name='show',
            name='likes',
            field=models.BigIntegerField(default=1523),
        ),
        migrations.AlterField(
            model_name='show',
            name='stars',
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name='show',
            name='views',
            field=models.BigIntegerField(default=2591),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 18, 23, 33, 12, 68000)),
        ),
    ]
