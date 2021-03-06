# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.MembershipPeriod')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.MembershipType')),
            ],
        ),
        migrations.RemoveField(
            model_name='membership',
            name='period',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='type',
        ),
        migrations.AddField(
            model_name='membership',
            name='membership',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='membership.PeriodType'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='periodtype',
            unique_together=set([('period', 'type')]),
        ),
    ]
