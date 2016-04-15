# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0006_auto_20160415_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataquality',
            name='num_addresses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataquality',
            name='num_districts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataquality',
            name='num_stations',
            field=models.IntegerField(default=0),
        ),
    ]
