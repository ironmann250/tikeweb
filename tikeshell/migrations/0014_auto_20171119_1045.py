# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-19 02:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikeshell', '0013_auto_20171118_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='tickettype_id',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='show',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 19, 10, 45, 22, 701000)),
        ),
        migrations.AlterField(
            model_name='show',
            name='likes',
            field=models.BigIntegerField(default=1575),
        ),
        migrations.AlterField(
            model_name='show',
            name='views',
            field=models.BigIntegerField(default=2303),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 19, 10, 45, 22, 709000)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='event_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='user_id',
            field=models.BigIntegerField(blank=True),
        ),
    ]