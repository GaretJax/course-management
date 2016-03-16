# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-12 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
        ('membership', '0005_auto_20160312_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='address',
            field=models.TextField(default='', verbose_name='address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cities.City', verbose_name='city'),
        ),
        migrations.AddField(
            model_name='contact',
            name='zip_code',
            field=models.CharField(default='', max_length=16, verbose_name='ZIP code'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='gender',
            field=models.NullBooleanField(choices=[(True, 'Male'), (False, 'Female')], verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='nationality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='cities.Country', verbose_name='nationality'),
        ),
    ]