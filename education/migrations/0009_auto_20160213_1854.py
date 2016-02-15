# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0008_auto_20151206_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('course', models.ForeignKey(related_name='sessions', to='education.Course')),
            ],
            options={
                'ordering': ('course', 'start'),
            },
        ),
        migrations.CreateModel(
            name='SessionCoach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filled_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('coach', models.ForeignKey(to='education.CourseCoach')),
                ('filled_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('session', models.ForeignKey(related_name='coaches', to='education.Session')),
            ],
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='course',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='location',
        ),
        migrations.AlterUniqueTogether(
            name='lessoncoach',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='lessoncoach',
            name='coach',
        ),
        migrations.RemoveField(
            model_name='lessoncoach',
            name='filled_by',
        ),
        migrations.RemoveField(
            model_name='lessoncoach',
            name='lesson',
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([]),
        ),
        migrations.DeleteModel(
            name='LessonCoach',
        ),
        migrations.AddField(
            model_name='session',
            name='location',
            field=models.ForeignKey(blank=True, to='education.Location', null=True),
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='lesson',
        ),
        migrations.AddField(
            model_name='attendance',
            name='session',
            field=models.ForeignKey(related_name='attendees', default=0, to='education.Session'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('session', 'registration')]),
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
        migrations.AlterUniqueTogether(
            name='sessioncoach',
            unique_together=set([('session', 'coach')]),
        ),
    ]
