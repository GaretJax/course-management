# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20151206_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCoach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.ForeignKey(to='education.Contact')),
                ('course', models.ForeignKey(related_name='coaches', to='education.Course')),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='lesson',
            field=models.ForeignKey(related_name='attendees', to='education.Lesson'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(related_name='lessons', to='education.Course'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='course',
            field=models.ForeignKey(related_name='registrations', to='education.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='coursecoach',
            unique_together=set([('course', 'contact')]),
        ),
    ]
