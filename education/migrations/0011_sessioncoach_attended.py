# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_auto_20160219_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessioncoach',
            name='attended',
            field=models.BooleanField(default=True),
        ),
    ]
