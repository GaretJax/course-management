# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 18:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_auto_20160213_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registration',
            options={'ordering': ('contact__first_name', 'contact__last_name')},
        ),
        migrations.AddField(
            model_name='attendance',
            name='attended',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='education.Contact'),
        ),
    ]
