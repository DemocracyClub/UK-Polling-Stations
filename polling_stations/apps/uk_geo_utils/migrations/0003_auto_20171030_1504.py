# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uk_geo_utils', '0002_onspd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onspd',
            name='id',
        ),
        migrations.AlterField(
            model_name='onspd',
            name='pcds',
            field=models.CharField(primary_key=True, max_length=8, blank=True, serialize=False),
        ),
    ]
