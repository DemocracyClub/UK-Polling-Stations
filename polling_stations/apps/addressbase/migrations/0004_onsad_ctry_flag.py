# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbase', '0003_auto_20170406_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='onsad',
            name='ctry_flag',
            field=models.CharField(max_length=1, blank=True),
        ),
    ]
