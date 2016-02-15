# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20151206_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
