# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('course', 'start')},
        ),
        migrations.AddField(
            model_name='course',
            name='end',
            field=models.DateField(default=datetime.datetime.max),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='location',
            field=models.ForeignKey(default=-1, to='education.Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='start',
            field=models.DateField(default=datetime.datetime.min),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='location',
            field=models.ForeignKey(blank=True, to='education.Location', null=True),
        ),
    ]
