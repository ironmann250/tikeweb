# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-19 02:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikeshell', '0014_auto_20171119_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 19, 10, 47, 30, 624000)),
        ),
        migrations.AlterField(
            model_name='show',
            name='likes',
            field=models.BigIntegerField(default=1450),
        ),
        migrations.AlterField(
            model_name='show',
            name='stars',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='show',
            name='views',
            field=models.BigIntegerField(default=2408),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 19, 10, 47, 30, 632000)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user_id',
            field=models.BigIntegerField(),
        ),
    ]
