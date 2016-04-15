# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0004_auto_20160121_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataquality',
            name='report',
            field=models.TextField(blank=True),
        ),
    ]
