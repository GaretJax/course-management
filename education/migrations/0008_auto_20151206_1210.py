# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0007_auto_20151206_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonCoach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filled_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterModelOptions(
            name='coursecoach',
            options={'verbose_name': 'coach', 'verbose_name_plural': 'coaches'},
        ),
        migrations.AddField(
            model_name='lessoncoach',
            name='coach',
            field=models.ForeignKey(to='education.CourseCoach'),
        ),
        migrations.AddField(
            model_name='lessoncoach',
            name='filled_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='lessoncoach',
            name='lesson',
            field=models.ForeignKey(related_name='coaches', to='education.Lesson'),
        ),
        migrations.AlterUniqueTogether(
            name='lessoncoach',
            unique_together=set([('lesson', 'coach')]),
        ),
    ]
