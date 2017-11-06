# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('councils', '0002_auto_20160121_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='council',
            name='council_type',
        ),
        migrations.RemoveField(
            model_name='council',
            name='location',
        ),
        migrations.RemoveField(
            model_name='council',
            name='mapit_id',
        ),
    ]
