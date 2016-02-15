# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20151206_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesson', models.ForeignKey(to='education.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.ForeignKey(to='education.Contact')),
                ('course', models.ForeignKey(to='education.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.OneToOneField(to='education.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='registration',
            field=models.ForeignKey(to='education.Registration'),
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set([('course', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('lesson', 'registration')]),
        ),
    ]
