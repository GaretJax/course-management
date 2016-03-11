# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 08:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filled_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('attended', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseCoach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Contact')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coaches', to='education.Course')),
            ],
            options={
                'verbose_name': 'coach',
                'verbose_name_plural': 'coaches',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='membership.Contact')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='education.Course')),
            ],
            options={
                'ordering': ('contact__first_name', 'contact__last_name'),
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='education.Course')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.Location')),
            ],
            options={
                'ordering': ('course', 'start'),
            },
        ),
        migrations.CreateModel(
            name='SessionCoach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filled_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('attended', models.BooleanField(default=True)),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.CourseCoach')),
                ('filled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coaches', to='education.Session')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='membership.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Location'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.Registration'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='filled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='education.Session'),
        ),
        migrations.AlterUniqueTogether(
            name='sessioncoach',
            unique_together=set([('session', 'attendee')]),
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set([('course', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursecoach',
            unique_together=set([('course', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('session', 'attendee')]),
        ),
    ]
